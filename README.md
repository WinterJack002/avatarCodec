# Avatar codec & postprocess code 
Put the source code of avatar animation codec & postprocess code here, consist of : 

- intra-coding of 52 BS(*__BlendShape__*) parameters, from sensors' original data to .bin, and from .bin to decoded data.
- inter-coding: add time prediction, do adjacent frame residual calculation.
- lossless-coding: depends on fixed precision, without quantization loss.
- post_analysis: some useful data process function.

> The usage of entropy coding method is **Golomb**. 
