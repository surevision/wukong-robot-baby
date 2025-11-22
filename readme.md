# 环境相关信息

## Wukong-Robot

requiremens.txt 中去掉了“funasr_onnx”库

## PaddleSpeech

paddlespeech avx版（检查自己的 cpu 是否支持 avx 指令集）
paddlepaddle==2.4.2
paddlespeech=1.2.0
numpy=1.23.1
inflect==4.0.0
typeguard==2.13.3
protobuf==3.20.0
ppdiffusers==0.9.0
faiss-cpu==1.8.0
scipy==1.10.1

noavx 版：

paddlepaddle==2.3.1
paddlespeech==1.2.0
inflect==4.0.0
typeguard==2.13.3

到 https://www.paddlepaddle.org.cn/documentation/docs/zh/2.4/install/Tables.html#whl-release 自行下载对应的 paddlepaddle 库，不要用最新的，paddlespeech 最高只支持到 paddlepaddle 2.5.1
