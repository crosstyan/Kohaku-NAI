import click
from enum import Enum
from loguru import logger
from request import GenerateRequest
import asyncio
import httpx
import json
from dataclasses import dataclass
from wildcard import get_tags, process_prompt
from pathlib import Path
from result import Result, Ok, Err


class AspectRatio(str, Enum):
    Horizontal = "h"
    Vertical = "v"
    UltraWide = "u"
    UltraTall = "t"
    Square = "s"


ar_map: dict[AspectRatio, tuple[int, int]] = {
    AspectRatio.Horizontal: (1216, 832),
    AspectRatio.Vertical: (832, 1216),
    AspectRatio.UltraWide: (1472, 704),
    AspectRatio.UltraTall: (704, 1472),
}


@click.command()
@click.option("--prompt", "-p", default="1girl", help="Prompt")
@click.option("--negative", "-n", default="bad quality", help="Negative prompt")
@click.option("--seed", "-s", default=-1, help="Seed")
@click.option("--scale", "-S", default=5.0, help="Scale, should be cfg scale")
@click.option("--width", "-w", help="Width")
@click.option("--height", "-h", help="Height")
@click.option("--steps", "-t", default=28, help="Steps")
@click.option(
    "--sampler",
    "-m",
    default="k_euler",
    help="Sampler",
    type=click.Choice([
        "k_euler",
        "k_euler_ancestral",
        "k_dpmpp_2s_ancestral",
        "k_dpmpp_2m",
        "k_dpmpp_sde",
        "ddim_v3",
    ]),
)
@click.option("--schedule", default="native", help="Schedule")
@click.option("--smea",
              is_flag=True,
              help="""
    Sinusoidal Multipass Euler Ancestral (SMEA) is a new sampler developed with
    the goal of improving overall coherency and quality, especially at higher
    resolutions.
    """)
@click.option("--dyn",
              is_flag=True,
              help="""
    SMEA DYN focuses less time on lower generations and begins to shine dynamically
    in the mid to high range of a generation. 
              """)
@click.option("--dyn-threshold", is_flag=True, help="Dyn threshold")
@click.option("--cfg-rescale", default=0, help="CFG rescale")
@click.option("--sub-folder",
              default="",
              help="Sub folder to save to, if permitted")
@click.option("--wildcard-dir",
              "-W",
              default=None,
              help="Wildcard dir",
              type=click.Path())
@click.option("--ar",
              type=click.Choice(AspectRatio),
              help="""
    Aspect ratio preset, would be ignored if width and height are specified
    """)
@click.option("--host",
              default="127.0.0.1:7000",
              help="the host (gen server) to connect to")
@click.option("--batch-count",
              "-b",
              default=1,
              help="the number of butches to generate")
@click.option("--auth", help="the auth password to use")
def main(
    prompt: str,
    negative: str,
    seed: int,
    scale: float,
    width: int | None,
    height: int | None,
    steps: int,
    sampler: str,
    schedule: str,
    smea: bool,
    dyn: bool,
    dyn_threshold: bool,
    cfg_rescale: bool,
    ar: AspectRatio | None,
    host: str,
    sub_folder: str,
    wildcard_dir: str,
    batch_count: int,
    auth: str | None,
):
    if wildcard_dir is not None:
        assert Path(wildcard_dir).exists(), "Wildcard dir must exist"
        assert Path(wildcard_dir).is_dir(), "Wildcard dir must be a directory"
        prompt = process_prompt(prompt, lambda x: get_tags(wildcard_dir, x))
        logger.info("processed prompt: {}".format(prompt))
    if auth is not None:
        raise NotImplementedError("Auth is not implemented yet")
    w = width
    h = height
    if ar is not None:
        if w is not None and h is not None:
            logger.warning(
                "Both width and height are specified, ignoring aspect ratio")
        else:
            w, h = ar_map[ar]
            logger.info(f"Using aspect ratio {ar.name} ({w}x{h})")
    if w is None or h is None:
        logger.warning(
            "Width or height is not specified, using default 1024x1024")
        w = 1024
        h = 1024
    smea_t = " smea" if smea else ""
    dyn_t = " dyn" if dyn else ""
    rescale = f" rescale={cfg_rescale}" if cfg_rescale else ""
    logger.info(
        f"{w}x{h}@{steps} with {sampler} ({schedule}{smea_t}{dyn_t}) at cfg {scale}{rescale}"
    )
    req = GenerateRequest(
        prompt=prompt,
        neg_prompt=negative,
        seed=seed,
        scale=scale,
        width=w,
        height=h,
        steps=steps,
        sampler=sampler,
        schedule=schedule,
        smea=smea,
        dyn=dyn,
        dyn_threshold=dyn_threshold,
        cfg_rescale=cfg_rescale,
    )
    # asyncio.run(send_req(host, req, sub_folder))
    total_timeout = batch_count * 30

    async def run() -> list[Result[bytes, GenError]]:
        promise = asyncio.gather(*[
            send_req(host, req, sub_folder, total_timeout)
            for _ in range(batch_count)
        ])
        await promise
        return promise.result()

    results = asyncio.run(run())
    for result in results:
        match result:
            case Ok(_):
                pass
            case Err(err):
                logger.error(f"Error: {err.error}")


@dataclass
class GenError:
    error: str
    status_code: int


async def send_req(host: str,
                   req: GenerateRequest,
                   sub_folder: str = "",
                   timeout=60) -> Result[bytes, GenError]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        host = f"http://{host}/gen" if not host.startswith("http") else host
        dump = req.model_dump()
        extra_infos = {}
        if sub_folder is not None:
            extra_infos["save_folder"] = sub_folder
        dump["extra_infos"] = json.dumps(extra_infos)
        resp = await client.post(host, json=dump)
        media_type = resp.headers.get("Content-Type", "")
        is_img = media_type.startswith("image")
        if not is_img:
            return Err(GenError(resp.text, resp.status_code))
        else:
            return Ok(resp.content)


if __name__ == "__main__":
    main()
