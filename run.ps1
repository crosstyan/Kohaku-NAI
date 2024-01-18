# python3 .\cli_client.py -p "tsubasa_tsubasa 1girl __color__ hair black serafuku" `
#  --sub-folder tsubasa_tsubasa -b 3 --ar v -F -W .\client_extensions\kohaku-nai-wildcards\wildcards\

## loli
# higeepon
# ken_(coffee_michikusa) 
# piyodera_mucha
# tsudero
# usashiro mani
# waero

## anime
# aoi_suzu
# dora_v_nu
# freedom_nakai
# goumudan
# hokori_sakuni
# mx2j
# pumpkinspicelatte
# kumasteam
# sincos
# sy4
# twin__tt_lsh_
# yamamoto_souichirou
# yutian_alice
# mdf_an

## classic good
# omone_hokoma_agm
# oouso
# nadegata
# kedama_milk
# torino_aqua

## suprising good
# beeeeen
# bae.c
# icecake
# jeneral
# iuui
# l_ract
# raiya_atelier
# hyouuma
# sunga2usagi
# tsubasa_tsubasa
# yd_(orange_maru) 
# yomu_(sgt_epper) 
# kie_(wylee2212) 
# zaphn

## good
# damda
# oekakizuki
# turisasu
# egami
# freng
# ginklaga
# greatodoggo
# haku89
# hayabusa
# hong_bai
# icwine
# kawakami_rokkaku
# laoan
# leviathan_(hikinito0902) 
# lillly
# mimoza_(96mimo414) 
# nagata_gata
# obaoba_(monkeyix) 
# qizhu
# rei_kun
# ririko__fhnngririko_
# sarena
# shibori_kasu
# soso__chlgksk110_
# yunsang
# z282g

## unique not xp
# lambda_(kusowarota) 
# lasterk
# mitsu_(mitsu_art) 
# muke__fz064_
# ninai
# nonohachi
# pottsness
# quasarcake
# rikume
# sage_joh
# seiru__prairie_
# suerte
# tamada_heijun
# uno_ryoku
# uo_denim
# waterring

## unique but idk
# oniilus
# re_shimashima
# rangen
# yukineko1018
# yurichtofen

## boring
# bigxixi
# catsmoon
# chela77
# cirilla_lin
# eto_(ikumika)
# fouriasensei
# gibun (sozoshu)
# greem_bang
# jack_dempa
# jjanda
# kataokasan
# iranon_(new_iranon) 
# nanaken_nana
# meion
# melopun
# muka_tsuku
# reel__riru_
# rhasta
# ru_zhai
# silver_bullet_(ecc12_8) 
# thanabis
# wu_ganlan_cai
# ying_yi

$artist = "aaaa_3"

$general = @"
1girl ahoge flat chest empty eyes closed mouth medium white hair hair between
eyes single sidelock red eyes, school uniform sailor collar pleated skirt, navel
midriff, no shoe, legs up, black thighhighs, white panties crotch seam, pussy
juice stain, invisible chair, foreshortening, black background 
"@


$general_nl = $general.Replace("`n", " ")

$suffix = "absurdres, year2022"

$prompt = $artist + " " + $general_nl + " " + $suffix

$uc = "bad quality"

python3 .\cli_client.py -p $prompt -n $uc `
 --sub-folder $artist -b 1 --ar s -F -W .\client_extensions\kohaku-nai-wildcards\wildcards\
