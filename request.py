from typing import Literal
from pydantic import BaseModel

ScheduleType = Literal["native", "karras", "exponential", "polyexponential"]

SamplerType = Literal["k_euler", "k_euler_ancestral", "k_dpmpp_2s_ancestral",
                      "k_dpmpp_2m", "k_dpmpp_sde", "ddim_v3"]

class GenerateRequest(BaseModel):
    prompt: str
    neg_prompt: str
    seed: int
    scale: float
    width: int
    height: int
    steps: int
    sampler: SamplerType
    schedule: ScheduleType
    smea: bool = False
    dyn: bool = False
    quality_toggle: bool = False
    dyn_threshold: bool = False
    cfg_rescale: float = 0.0
    img_sub_folder: str = ""
    extra_infos: str = ""
