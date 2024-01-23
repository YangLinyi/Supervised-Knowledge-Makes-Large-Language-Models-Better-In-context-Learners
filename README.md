# Supervised Knowledge Makes Large Language Models Better In-context Learners

<div align="center">
  <a href=" ">
    <img src="figures_md/supercontext.pdf" alt="" width="480">
  </a>
  </br>
  <a>Linyi Yang<sup>*1,2</sup></a>&emsp;
  <a>Shuibai Zhang<sup>*1</sup></a>&emsp;
  <a>Zhuohao Yu<sup>*3</sup></a>&emsp;
  </br>
  <a>Guangsheng Bao<sup>2</sup></a>&emsp;
  <a>Yidong Wang<sup>1,3</sup></a>&emsp;
  <a>Jindong Wang<sup>4</sup></a>&emsp;
  <a>Ruochen Xu<sup>4</sup></a>&emsp;
  <a>Wei Ye<sup>1</sup></a>&emsp;
  </br>
  <a>Xing Xie<sup>4</sup></a>&emsp;
  <a>Weizhu Chen<sup>4</sup></a>&emsp;
  <a>Yue Zhang<sup>†1,2</sup></a>&emsp;
  <div>
    </br>
    *: Co-first Authors   †: Corresponding Authors
  </div>
  <p> </br> <sup>1</sup> School of Engineering, Westlake University, <sup>2</sup> Westlake Institute for Advanced Study,</br> <sup>3</sup> 
Peking University, <sup>4</sup> Microsoft  
</div>


## Overview
This is the official repository for Supervised Knowledge Makes Large Language Models Better In-context Learners.

Paper: [Supervised Knowledge Makes Large Language Models Better In-context Learners](https://arxiv.org/abs/2312.15918)

Large Language Models (LLMs) exhibit emerging in-context learning abilities through prompt engineering. The recent progress in large-scale generative models has further expanded their use in real-world language applications. However, the critical challenge of improving the generalizability and factuality of LLMs in natural language understanding and question answering remains under-explored. While previous in-context learning research has focused on enhancing models to adhere to users' specific instructions and quality expectations, and to avoid undesired outputs, little to no work has explored the use of task-Specific fine-tuned Language Models (SLMs) to improve LLMs' in-context learning during the inference stage. Our primary contribution is the establishment of a simple yet effective framework that enhances the reliability of LLMs as it: 1) generalizes out-of-distribution data, 2) elucidates how LLMs benefit from discriminative models, and 3) minimizes hallucinations in generative tasks. Using our proposed plug-in method, enhanced versions of Llama 2 and ChatGPT surpass their original versions regarding generalizability and factuality. **We offer a comprehensive suite of resources, including 16 curated datasets, prompts, model checkpoints, and LLM outputs across 9 distinct tasks.** Our empirical analysis sheds light on the advantages of incorporating discriminative models into LLMs and highlights the potential of our methodology in fostering more reliable LLMs.

![img](figures_md/example_prompt.pdf)

This repository contains:

- The codes for implementing SuperContext
- The prompts used for each task
- The model weights of Pre-trained Language Models
- The codes and configs for fine-tuning models.

## News 
- [2024/01/23] SuperContext was accepted to ICLR 2024!
- [2023/12/27] Our paper has been collected by HuggingFace's daily selection on Twitter.


## **Conrtibuting**

We welcome contributions to SuperContext. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch with your changes.
3. Submit a pull request with a clear description of your changes.


## **Citation**

```Plain
@inproceedings{yang2024supervised,
  title={Supervised Knowledge Makes Large Language Models Better In-context Learners},
  author={Linyi Yang, Shuibai Zhang, Zhuohao Yu, Guangsheng Bao, Yidong Wang, Jindong Wang, Ruochen Xu, Wei Ye, Xing Xie, Weizhu Chen, Yue Zhang},
  booktitle={The Eighteenth International Conference on Learning Representations (ICLR 2024)},
  year={2024}
}
```

## **License**

For model weights of LLaMA-based models, we follow the LLaMA license. See MODEL_LICENSE.

The rest of this repo is under Apache License 2.0. See LICENSE.
