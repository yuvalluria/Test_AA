#!/usr/bin/env python3
"""
Script to add all open-source models from the comprehensive list
"""
import json
from typing import Dict, List

# Models data extracted from the list
MODELS_DATA = [
    {"name": "Kimi K2 Thinking", "provider": "Moonshot AI", "intelligence": 67, "params": "1.0KB (32B active)", "dataset": "Kimi K2 training dataset"},
    {"name": "MiniMax-M2", "provider": "MiniMax", "intelligence": 61, "params": "230B (10B active)", "dataset": "MiniMax training dataset"},
    {"name": "gpt-oss-120B (high)", "provider": "OpenAI", "intelligence": 61, "params": "117B (5.1B active)", "dataset": "GPT-OSS training dataset"},
    {"name": "DeepSeek V3.1 Terminus (Reasoning)", "provider": "DeepSeek", "intelligence": 58, "params": "685B (37B active)", "dataset": "DeepSeek V3.1 training dataset"},
    {"name": "Qwen3 235B A22B 2507 (Reasoning)", "provider": "Alibaba", "intelligence": 57, "params": "235B (22B active)", "dataset": "Qwen3 training dataset"},
    {"name": "DeepSeek V3.2 Exp (Reasoning)", "provider": "DeepSeek", "intelligence": 57, "params": "685B (37.0B active)", "dataset": "DeepSeek V3.2 training dataset"},
    {"name": "GLM-4.6 (Reasoning)", "provider": "Z AI", "intelligence": 56, "params": "357B (32B active)", "dataset": "GLM-4.6 training dataset"},
    {"name": "Qwen3 VL 235B A22B (Reasoning)", "provider": "Alibaba", "intelligence": 54, "params": "235B (22.0B active)", "dataset": "Qwen3 VL training dataset"},
    {"name": "Qwen3 Next 80B A3B (Reasoning)", "provider": "Alibaba", "intelligence": 54, "params": "80B (3B active)", "dataset": "Qwen3 Next training dataset"},
    {"name": "DeepSeek V3.1 (Reasoning)", "provider": "DeepSeek", "intelligence": 54, "params": "685B (37.0B active)", "dataset": "DeepSeek V3.1 training dataset"},
    {"name": "gpt-oss-20B (high)", "provider": "OpenAI", "intelligence": 52, "params": "21B (3.6B active)", "dataset": "GPT-OSS training dataset"},
    {"name": "DeepSeek R1 0528 (May '25)", "provider": "DeepSeek", "intelligence": 52, "params": "685B (37B active)", "dataset": "DeepSeek R1 training dataset"},
    {"name": "Qwen3 VL 32B (Reasoning)", "provider": "Alibaba", "intelligence": 52, "params": "33.4B", "dataset": "Qwen3 VL training dataset"},
    {"name": "Seed-OSS-36B-Instruct", "provider": "ByteDance Seed", "intelligence": 52, "params": "36.2B", "dataset": "Seed training dataset"},
    {"name": "Apriel-v1.5-15B-Thinker", "provider": "ServiceNow", "intelligence": 52, "params": "15B", "dataset": "Apriel training dataset"},
    {"name": "GLM-4.5 (Reasoning)", "provider": "Z AI", "intelligence": 51, "params": "355B (32B active)", "dataset": "GLM-4.5 training dataset"},
    {"name": "Kimi K2 0905", "provider": "Moonshot AI", "intelligence": 50, "params": "1.0KB (32.0B active)", "dataset": "Kimi K2 training dataset"},
    {"name": "GLM-4.5-Air", "provider": "Z AI", "intelligence": 49, "params": "106B (12B active)", "dataset": "GLM-4.5 training dataset"},
    {"name": "Kimi K2", "provider": "Moonshot AI", "intelligence": 48, "params": "1.0KB (32B active)", "dataset": "Kimi K2 training dataset"},
    {"name": "gpt-oss-120B (low)", "provider": "OpenAI", "intelligence": 48, "params": "117B (5.1B active)", "dataset": "GPT-OSS training dataset"},
    {"name": "Qwen3 30B A3B 2507 (Reasoning)", "provider": "Alibaba", "intelligence": 46, "params": "30.5B (3.3B active)", "dataset": "Qwen3 training dataset"},
    {"name": "DeepSeek V3.2 Exp (Non-reasoning)", "provider": "DeepSeek", "intelligence": 46, "params": "685B (37.0B active)", "dataset": "DeepSeek V3.2 training dataset"},
    {"name": "MiniMax M1 80k", "provider": "MiniMax", "intelligence": 46, "params": "456B (45.9B active)", "dataset": "MiniMax M1 training dataset"},
    {"name": "DeepSeek V3.1 Terminus (Non-reasoning)", "provider": "DeepSeek", "intelligence": 46, "params": "685B (37B active)", "dataset": "DeepSeek V3.1 training dataset"},
    {"name": "Qwen3 235B A22B 2507 Instruct", "provider": "Alibaba", "intelligence": 45, "params": "235B (22.0B active)", "dataset": "Qwen3 training dataset"},
    {"name": "Qwen3 VL 30B A3B (Reasoning)", "provider": "Alibaba", "intelligence": 45, "params": "30B (3.0B active)", "dataset": "Qwen3 VL training dataset"},
    {"name": "Llama Nemotron Super 49B v1.5 (Reasoning)", "provider": "NVIDIA", "intelligence": 45, "params": "49B", "dataset": "Llama Nemotron training dataset"},
    {"name": "Qwen3 Next 80B A3B Instruct", "provider": "Alibaba", "intelligence": 45, "params": "80B (3B active)", "dataset": "Qwen3 Next training dataset"},
    {"name": "Ling-1T", "provider": "InclusionAI", "intelligence": 45, "params": "1.0KB (50.0B active)", "dataset": "Ling training dataset"},
    {"name": "DeepSeek V3.1 (Non-reasoning)", "provider": "DeepSeek", "intelligence": 45, "params": "685B (37B active)", "dataset": "DeepSeek V3.1 training dataset"},
    {"name": "GLM-4.6 (Non-reasoning)", "provider": "Z AI", "intelligence": 45, "params": "357B (32B active)", "dataset": "GLM-4.6 training dataset"},
    {"name": "gpt-oss-20B (low)", "provider": "OpenAI", "intelligence": 44, "params": "21B (3.6B active)", "dataset": "GPT-OSS training dataset"},
    {"name": "Qwen3 VL 235B A22B Instruct", "provider": "Alibaba", "intelligence": 44, "params": "235B (22.0B active)", "dataset": "Qwen3 VL training dataset"},
    {"name": "DeepSeek R1 (Jan '25)", "provider": "DeepSeek", "intelligence": 44, "params": "685B (37B active)", "dataset": "DeepSeek R1 training dataset"},
    {"name": "Qwen3 4B 2507 (Reasoning)", "provider": "Alibaba", "intelligence": 43, "params": "4.02B", "dataset": "Qwen3 training dataset"},
    {"name": "Magistral Small 1.2", "provider": "Mistral", "intelligence": 43, "params": "24B", "dataset": "Mistral training dataset"},
    {"name": "EXAONE 4.0 32B (Reasoning)", "provider": "LG AI Research", "intelligence": 43, "params": "32B", "dataset": "EXAONE training dataset"},
    {"name": "Qwen3 Coder 480B A35B Instruct", "provider": "Alibaba", "intelligence": 42, "params": "480B (35.0B active)", "dataset": "Qwen3 Coder training dataset"},
    {"name": "Ring-1T", "provider": "InclusionAI", "intelligence": 42, "params": "1.0KB (50.0B active)", "dataset": "Ring training dataset"},
    {"name": "Qwen3 235B A22B (Reasoning)", "provider": "Alibaba", "intelligence": 42, "params": "235B (22B active)", "dataset": "Qwen3 training dataset"},
    {"name": "Hermes 4 - Llama-3.1 405B (Reasoning)", "provider": "Nous Research", "intelligence": 42, "params": "406B", "dataset": "Hermes 4 training dataset"},
    {"name": "DeepSeek V3 0324", "provider": "DeepSeek", "intelligence": 41, "params": "671B (37B active)", "dataset": "DeepSeek V3 training dataset"},
    {"name": "Qwen3 VL 32B Instruct", "provider": "Alibaba", "intelligence": 41, "params": "33.4B", "dataset": "Qwen3 VL training dataset"},
    {"name": "MiniMax M1 40k", "provider": "MiniMax", "intelligence": 40, "params": "456B (45.9B active)", "dataset": "MiniMax M1 training dataset"},
    {"name": "Qwen3 Omni 30B A3B (Reasoning)", "provider": "Alibaba", "intelligence": 40, "params": "35.3B (3.0B active)", "dataset": "Qwen3 Omni training dataset"},
    {"name": "Ring-flash-2.0", "provider": "InclusionAI", "intelligence": 40, "params": "103B (6.1B active)", "dataset": "Ring training dataset"},
    {"name": "Hermes 4 - Llama-3.1 70B (Reasoning)", "provider": "Nous Research", "intelligence": 39, "params": "70.6B", "dataset": "Hermes 4 training dataset"},
    {"name": "Qwen3 32B (Reasoning)", "provider": "Alibaba", "intelligence": 39, "params": "32.8B", "dataset": "Qwen3 training dataset"},
    {"name": "Llama 3.1 Nemotron Ultra 253B v1 (Reasoning)", "provider": "NVIDIA", "intelligence": 38, "params": "253B", "dataset": "Llama Nemotron training dataset"},
    {"name": "Qwen3 VL 30B A3B Instruct", "provider": "Alibaba", "intelligence": 38, "params": "30B (3.0B active)", "dataset": "Qwen3 VL training dataset"},
    {"name": "Ling-flash-2.0", "provider": "InclusionAI", "intelligence": 38, "params": "103B (6.1B active)", "dataset": "Ling training dataset"},
    {"name": "QwQ 32B", "provider": "Alibaba", "intelligence": 38, "params": "32.8B", "dataset": "QwQ training dataset"},
    {"name": "NVIDIA Nemotron Nano 9B V2 (Reasoning)", "provider": "NVIDIA", "intelligence": 37, "params": "9B", "dataset": "NVIDIA Nemotron training dataset"},
    {"name": "GLM-4.5V (Reasoning)", "provider": "Z AI", "intelligence": 37, "params": "108B (12.0B active)", "dataset": "GLM-4.5 training dataset"},
    {"name": "Qwen3 30B A3B 2507 Instruct", "provider": "Alibaba", "intelligence": 37, "params": "30.5B (3.3B active)", "dataset": "Qwen3 training dataset"},
    {"name": "Qwen3 30B A3B (Reasoning)", "provider": "Alibaba", "intelligence": 37, "params": "30.5B (3.3B active)", "dataset": "Qwen3 training dataset"},
    {"name": "NVIDIA Nemotron Nano 9B V2 (Non-reasoning)", "provider": "NVIDIA", "intelligence": 36, "params": "9B", "dataset": "NVIDIA Nemotron training dataset"},
    {"name": "Qwen3 14B (Reasoning)", "provider": "Alibaba", "intelligence": 36, "params": "14.8B", "dataset": "Qwen3 training dataset"},
    {"name": "Llama 4 Maverick", "provider": "Meta", "intelligence": 36, "params": "402B (17B active)", "dataset": "Llama 4 training dataset"},
    {"name": "Llama 3.3 Nemotron Super 49B v1 (Reasoning)", "provider": "NVIDIA", "intelligence": 35, "params": "49B", "dataset": "Llama Nemotron training dataset"},
    {"name": "Qwen3 Coder 30B A3B Instruct", "provider": "Alibaba", "intelligence": 33, "params": "30.5B (3.3B active)", "dataset": "Qwen3 Coder training dataset"},
    {"name": "ERNIE 4.5 300B A47B", "provider": "Baidu", "intelligence": 33, "params": "300B (47.0B active)", "dataset": "ERNIE training dataset"},
    {"name": "DeepSeek R1 Distill Qwen 32B", "provider": "DeepSeek", "intelligence": 33, "params": "32B", "dataset": "DeepSeek R1 training dataset"},
    {"name": "Hermes 4 - Llama-3.1 405B (Non-reasoning)", "provider": "Nous Research", "intelligence": 33, "params": "406B", "dataset": "Hermes 4 training dataset"},
    {"name": "DeepSeek V3 (Dec '24)", "provider": "DeepSeek", "intelligence": 32, "params": "671B (37B active)", "dataset": "DeepSeek V3 training dataset"},
    {"name": "Qwen3 VL 8B (Reasoning)", "provider": "Alibaba", "intelligence": 32, "params": "8.77B", "dataset": "Qwen3 VL training dataset"},
    {"name": "Magistral Small 1", "provider": "Mistral", "intelligence": 32, "params": "23.6B", "dataset": "Mistral training dataset"},
    {"name": "DeepSeek R1 0528 Qwen3 8B", "provider": "DeepSeek", "intelligence": 31, "params": "8.19B", "dataset": "DeepSeek R1 training dataset"},
    {"name": "Qwen3 4B 2507 Instruct", "provider": "Alibaba", "intelligence": 30, "params": "4.02B", "dataset": "Qwen3 training dataset"},
    {"name": "EXAONE 4.0 32B (Non-reasoning)", "provider": "LG AI Research", "intelligence": 30, "params": "32B", "dataset": "EXAONE training dataset"},
    {"name": "Qwen3 Omni 30B A3B Instruct", "provider": "Alibaba", "intelligence": 30, "params": "35.3B (3.0B active)", "dataset": "Qwen3 Omni training dataset"},
    {"name": "Qwen3 235B A22B (Non-reasoning)", "provider": "Alibaba", "intelligence": 30, "params": "235B (22B active)", "dataset": "Qwen3 training dataset"},
    {"name": "DeepSeek R1 Distill Llama 70B", "provider": "DeepSeek", "intelligence": 30, "params": "70B", "dataset": "DeepSeek R1 training dataset"},
    {"name": "DeepSeek R1 Distill Qwen 14B", "provider": "DeepSeek", "intelligence": 30, "params": "14B", "dataset": "DeepSeek R1 training dataset"},
    {"name": "Qwen3 14B (Non-reasoning)", "provider": "Alibaba", "intelligence": 29, "params": "14.8B", "dataset": "Qwen3 training dataset"},
    {"name": "Mistral Small 3.2", "provider": "Mistral", "intelligence": 29, "params": "24B", "dataset": "Mistral training dataset"},
    {"name": "Qwen2.5 Instruct 72B", "provider": "Alibaba", "intelligence": 29, "params": "72B", "dataset": "Qwen2.5 training dataset"},
    {"name": "MiniMax-Text-01", "provider": "MiniMax", "intelligence": 28, "params": "456B (45.9B active)", "dataset": "MiniMax training dataset"},
    {"name": "Qwen3 8B (Reasoning)", "provider": "Alibaba", "intelligence": 28, "params": "8.19B", "dataset": "Qwen3 training dataset"},
    {"name": "Llama 4 Scout", "provider": "Meta", "intelligence": 28, "params": "109B (17B active)", "dataset": "Llama 4 training dataset"},
    {"name": "Llama 3.1 Instruct 405B", "provider": "Meta", "intelligence": 28, "params": "405B", "dataset": "Llama 3.1 training dataset"},
    {"name": "QwQ 32B-Preview", "provider": "Alibaba", "intelligence": 28, "params": "32.8B", "dataset": "QwQ training dataset"},
    {"name": "Llama 3.3 Instruct 70B", "provider": "Meta", "intelligence": 28, "params": "70B", "dataset": "Llama 3.3 training dataset"},
    {"name": "Ling-mini-2.0", "provider": "InclusionAI", "intelligence": 28, "params": "16.3B (1.4B active)", "dataset": "Ling training dataset"},
    {"name": "Qwen3 VL 4B (Reasoning)", "provider": "Alibaba", "intelligence": 27, "params": "4.44B", "dataset": "Qwen3 VL training dataset"},
    {"name": "Devstral Small (Jul '25)", "provider": "Mistral", "intelligence": 27, "params": "24B", "dataset": "Mistral training dataset"},
    {"name": "Qwen3 VL 8B Instruct", "provider": "Alibaba", "intelligence": 27, "params": "8.77B", "dataset": "Qwen3 VL training dataset"},
    {"name": "Command A", "provider": "Cohere", "intelligence": 27, "params": "111B", "dataset": "Cohere training dataset"},
    {"name": "Mistral Large 2 (Nov '24)", "provider": "Mistral", "intelligence": 27, "params": "123B", "dataset": "Mistral training dataset"},
    {"name": "Exaone 4.0 1.2B (Reasoning)", "provider": "LG AI Research", "intelligence": 27, "params": "1.28B", "dataset": "EXAONE training dataset"},
    {"name": "Llama Nemotron Super 49B v1.5 (Non-reasoning)", "provider": "NVIDIA", "intelligence": 27, "params": "49B", "dataset": "Llama Nemotron training dataset"},
    {"name": "Qwen3 30B A3B (Non-reasoning)", "provider": "Alibaba", "intelligence": 26, "params": "30.5B (3.3B active)", "dataset": "Qwen3 training dataset"},
    {"name": "Qwen3 32B (Non-reasoning)", "provider": "Alibaba", "intelligence": 26, "params": "32.8B", "dataset": "Qwen3 training dataset"},
    {"name": "Llama 3.1 Nemotron Nano 4B v1.1 (Reasoning)", "provider": "NVIDIA", "intelligence": 26, "params": "4.51B", "dataset": "Llama Nemotron training dataset"},
    {"name": "GLM-4.5V (Non-reasoning)", "provider": "Z AI", "intelligence": 26, "params": "108B (12.0B active)", "dataset": "GLM-4.5 training dataset"},
    {"name": "Reka Flash 3", "provider": "Reka AI", "intelligence": 26, "params": "21B", "dataset": "Reka training dataset"},
    {"name": "Llama 3.3 Nemotron Super 49B v1 (Non-reasoning)", "provider": "NVIDIA", "intelligence": 26, "params": "49B", "dataset": "Llama Nemotron training dataset"},
    {"name": "Qwen3 4B (Reasoning)", "provider": "Alibaba", "intelligence": 26, "params": "4.02B", "dataset": "Qwen3 training dataset"},
    {"name": "Llama 3.1 Tulu3 405B", "provider": "Allen Institute for AI", "intelligence": 25, "params": "405B", "dataset": "Tulu3 training dataset"},
    {"name": "Qwen3 VL 4B Instruct", "provider": "Alibaba", "intelligence": 25, "params": "4.44B", "dataset": "Qwen3 VL training dataset"},
    {"name": "Pixtral Large", "provider": "Mistral", "intelligence": 25, "params": "124B", "dataset": "Mistral training dataset"},
    {"name": "Grok 2 (Dec '24)", "provider": "xAI", "intelligence": 25, "params": "270B", "dataset": "Grok training dataset"},
    {"name": "Hermes 4 - Llama-3.1 70B (Non-reasoning)", "provider": "Nous Research", "intelligence": 24, "params": "70.6B", "dataset": "Hermes 4 training dataset"},
    {"name": "Llama 3.1 Nemotron Instruct 70B", "provider": "NVIDIA", "intelligence": 24, "params": "70B", "dataset": "Llama Nemotron training dataset"},
    {"name": "Mistral Small 3.1", "provider": "Mistral", "intelligence": 23, "params": "24B", "dataset": "Mistral training dataset"},
    {"name": "Qwen3 8B (Non-reasoning)", "provider": "Alibaba", "intelligence": 23, "params": "8.19B", "dataset": "Qwen3 training dataset"},
    {"name": "Qwen2.5 Instruct 32B", "provider": "Alibaba", "intelligence": 23, "params": "32B", "dataset": "Qwen2.5 training dataset"},
    {"name": "Granite 4.0 H Small", "provider": "IBM", "intelligence": 23, "params": "32B (9B active)", "dataset": "Granite training dataset"},
    {"name": "Phi-4", "provider": "Microsoft Azure", "intelligence": 23, "params": "14B", "dataset": "Phi training dataset"},
    {"name": "Llama 3.1 Instruct 70B", "provider": "Meta", "intelligence": 23, "params": "70B", "dataset": "Llama 3.1 training dataset"},
    {"name": "Qwen3 1.7B (Reasoning)", "provider": "Alibaba", "intelligence": 22, "params": "2.03B", "dataset": "Qwen3 training dataset"},
    {"name": "Mistral Large 2 (Jul '24)", "provider": "Mistral", "intelligence": 22, "params": "123B", "dataset": "Mistral training dataset"},
    {"name": "Gemma 3 27B Instruct", "provider": "Google", "intelligence": 22, "params": "27.4B", "dataset": "Gemma 3 training dataset"},
    {"name": "Qwen2.5 Coder Instruct 32B", "provider": "Alibaba", "intelligence": 22, "params": "32B", "dataset": "Qwen2.5 Coder training dataset"},
    {"name": "Mistral Small 3", "provider": "Mistral", "intelligence": 21, "params": "24B", "dataset": "Mistral training dataset"},
    {"name": "Jamba Reasoning 3B", "provider": "AI21 Labs", "intelligence": 21, "params": "3B", "dataset": "Jamba training dataset"},
    {"name": "Jamba 1.7 Large", "provider": "AI21 Labs", "intelligence": 21, "params": "398B (94.0B active)", "dataset": "Jamba training dataset"},
    {"name": "DeepSeek-V2.5 (Dec '24)", "provider": "DeepSeek", "intelligence": 21, "params": "236B (21B active)", "dataset": "DeepSeek V2.5 training dataset"},
    {"name": "Qwen3 4B (Non-reasoning)", "provider": "Alibaba", "intelligence": 21, "params": "4.02B", "dataset": "Qwen3 training dataset"},
    {"name": "Exaone 4.0 1.2B (Non-reasoning)", "provider": "LG AI Research", "intelligence": 20, "params": "1.28B", "dataset": "EXAONE training dataset"},
    {"name": "Gemma 3 12B Instruct", "provider": "Google", "intelligence": 20, "params": "12.2B", "dataset": "Gemma 3 training dataset"},
    {"name": "DeepSeek-V2.5", "provider": "DeepSeek", "intelligence": 20, "params": "236B (21B active)", "dataset": "DeepSeek V2.5 training dataset"},
    {"name": "Devstral Small (May '25)", "provider": "Mistral", "intelligence": 20, "params": "23.6B", "dataset": "Mistral training dataset"},
    {"name": "DeepSeek R1 Distill Llama 8B", "provider": "DeepSeek", "intelligence": 19, "params": "8B", "dataset": "DeepSeek R1 training dataset"},
    {"name": "R1 1776", "provider": "Perplexity", "intelligence": 19, "params": "671B (37B active)", "dataset": "Perplexity training dataset"},
    {"name": "Llama 3.2 Instruct 90B (Vision)", "provider": "Meta", "intelligence": 19, "params": "90B", "dataset": "Llama 3.2 training dataset"},
    {"name": "Solar Mini", "provider": "Upstage", "intelligence": 19, "params": "10.7B", "dataset": "Solar training dataset"},
    {"name": "Grok-1", "provider": "xAI", "intelligence": 18, "params": "314B (78B active)", "dataset": "Grok training dataset"},
    {"name": "Qwen2 Instruct 72B", "provider": "Alibaba", "intelligence": 18, "params": "72B", "dataset": "Qwen2 training dataset"},
    {"name": "LFM2 8B A1B", "provider": "Liquid AI", "intelligence": 17, "params": "8.34B (1.5B active)", "dataset": "LFM2 training dataset"},
    {"name": "Gemma 2 27B", "provider": "Google", "intelligence": 17, "params": "27.2B", "dataset": "Gemma 2 training dataset"},
    {"name": "Llama 3.1 Instruct 8B", "provider": "Meta", "intelligence": 17, "params": "8B", "dataset": "Llama 3.1 training dataset"},
    {"name": "Granite 4.0 Micro", "provider": "IBM", "intelligence": 16, "params": "3B", "dataset": "Granite training dataset"},
    {"name": "Phi-4 Mini Instruct", "provider": "Microsoft Azure", "intelligence": 16, "params": "3.84B", "dataset": "Phi training dataset"},
    {"name": "DeepHermes 3 - Mistral 24B Preview (Non-reasoning)", "provider": "Nous Research", "intelligence": 16, "params": "24B", "dataset": "DeepHermes training dataset"},
    {"name": "Llama 3.2 Instruct 11B (Vision)", "provider": "Meta", "intelligence": 16, "params": "11B", "dataset": "Llama 3.2 training dataset"},
    {"name": "Gemma 3n E4B Instruct", "provider": "Google", "intelligence": 15, "params": "8.39B (4.0B active)", "dataset": "Gemma 3 training dataset"},
    {"name": "Granite 3.3 8B (Non-reasoning)", "provider": "IBM", "intelligence": 15, "params": "8.17B", "dataset": "Granite training dataset"},
    {"name": "Jamba 1.5 Large", "provider": "AI21 Labs", "intelligence": 15, "params": "398B (94B active)", "dataset": "Jamba training dataset"},
    {"name": "Jamba 1.7 Mini", "provider": "AI21 Labs", "intelligence": 15, "params": "52B (12.0B active)", "dataset": "Jamba training dataset"},
    {"name": "Gemma 3 4B Instruct", "provider": "Google", "intelligence": 15, "params": "4.3B", "dataset": "Gemma 3 training dataset"},
    {"name": "Hermes 3 - Llama-3.1 70B", "provider": "Nous Research", "intelligence": 15, "params": "70.6B", "dataset": "Hermes training dataset"},
    {"name": "DeepSeek-Coder-V2", "provider": "DeepSeek", "intelligence": 15, "params": "236B (21B active)", "dataset": "DeepSeek Coder training dataset"},
    {"name": "Qwen3 1.7B (Non-reasoning)", "provider": "Alibaba", "intelligence": 14, "params": "2.03B", "dataset": "Qwen3 training dataset"},
    {"name": "Phi-3 Medium Instruct 14B", "provider": "Microsoft Azure", "intelligence": 14, "params": "14B", "dataset": "Phi training dataset"},
    {"name": "OLMo 2 32B", "provider": "Allen Institute for AI", "intelligence": 14, "params": "32.2B", "dataset": "OLMo training dataset"},
    {"name": "Jamba 1.6 Large", "provider": "AI21 Labs", "intelligence": 14, "params": "398B (94B active)", "dataset": "Jamba training dataset"},
    {"name": "Qwen3 0.6B (Reasoning)", "provider": "Alibaba", "intelligence": 14, "params": "0.752B", "dataset": "Qwen3 training dataset"},
    {"name": "Granite 4.0 H 1B", "provider": "IBM", "intelligence": 14, "params": "1.5B", "dataset": "Granite training dataset"},
    {"name": "Aya Expanse 32B", "provider": "Cohere", "intelligence": 14, "params": "32B", "dataset": "Cohere training dataset"},
    {"name": "Granite 4.0 1B", "provider": "IBM", "intelligence": 13, "params": "1.6B", "dataset": "Granite training dataset"},
    {"name": "Llama 3 Instruct 70B", "provider": "Meta", "intelligence": 13, "params": "70B", "dataset": "Llama 3 training dataset"},
    {"name": "Mistral Small (Sep '24)", "provider": "Mistral", "intelligence": 13, "params": "22B", "dataset": "Mistral training dataset"},
    {"name": "Phi-3 Mini Instruct 3.8B", "provider": "Microsoft Azure", "intelligence": 13, "params": "3.8B", "dataset": "Phi training dataset"},
    {"name": "Gemma 3n E4B Instruct Preview (May '25)", "provider": "Google", "intelligence": 13, "params": "8.39B (4B active)", "dataset": "Gemma 3 training dataset"},
    {"name": "Phi-4 Multimodal Instruct", "provider": "Microsoft Azure", "intelligence": 12, "params": "5.6B", "dataset": "Phi training dataset"},
    {"name": "Ministral 8B", "provider": "Mistral", "intelligence": 12, "params": "8B", "dataset": "Mistral training dataset"},
    {"name": "Qwen2.5 Coder Instruct 7B", "provider": "Alibaba", "intelligence": 12, "params": "7.62B", "dataset": "Qwen2.5 Coder training dataset"},
    {"name": "LFM2 2.6B", "provider": "Liquid AI", "intelligence": 12, "params": "2.57B", "dataset": "LFM2 training dataset"},
    {"name": "Mixtral 8x22B Instruct", "provider": "Mistral", "intelligence": 12, "params": "141B (39B active)", "dataset": "Mixtral training dataset"},
    {"name": "Llama 2 Chat 7B", "provider": "Meta", "intelligence": 11, "params": "7B", "dataset": "Llama 2 training dataset"},
    {"name": "Gemma 3n E2B Instruct", "provider": "Google", "intelligence": 11, "params": "5.98B (2.0B active)", "dataset": "Gemma 3 training dataset"},
    {"name": "Llama 3.2 Instruct 3B", "provider": "Meta", "intelligence": 11, "params": "3B", "dataset": "Llama 3.2 training dataset"},
    {"name": "Qwen3 0.6B (Non-reasoning)", "provider": "Alibaba", "intelligence": 11, "params": "0.752B", "dataset": "Qwen3 training dataset"},
    {"name": "Qwen1.5 Chat 110B", "provider": "Alibaba", "intelligence": 11, "params": "110B", "dataset": "Qwen1.5 training dataset"},
    {"name": "Aya Expanse 8B", "provider": "Cohere", "intelligence": 10, "params": "8B", "dataset": "Cohere training dataset"},
    {"name": "LFM2 1.2B", "provider": "Liquid AI", "intelligence": 10, "params": "1.17B", "dataset": "LFM2 training dataset"},
    {"name": "OLMo 2 7B", "provider": "Allen Institute for AI", "intelligence": 10, "params": "7.3B", "dataset": "OLMo training dataset"},
    {"name": "Molmo 7B-D", "provider": "Allen Institute for AI", "intelligence": 9, "params": "8.02B", "dataset": "Molmo training dataset"},
    {"name": "Pixtral 12B (2409)", "provider": "Mistral", "intelligence": 9, "params": "12B", "dataset": "Mistral training dataset"},
    {"name": "Llama 3.2 Instruct 1B", "provider": "Meta", "intelligence": 9, "params": "1B", "dataset": "Llama 3.2 training dataset"},
    {"name": "DeepSeek R1 Distill Qwen 1.5B", "provider": "DeepSeek", "intelligence": 9, "params": "1.5B", "dataset": "DeepSeek R1 training dataset"},
    {"name": "DeepSeek-V2-Chat", "provider": "DeepSeek", "intelligence": 9, "params": "236B (21B active)", "dataset": "DeepSeek V2 training dataset"},
    {"name": "Granite 4.0 H 350M", "provider": "IBM", "intelligence": 8, "params": "0.34B", "dataset": "Granite training dataset"},
    {"name": "Gemma 2 9B", "provider": "Google", "intelligence": 8, "params": "9B", "dataset": "Gemma 2 training dataset"},
    {"name": "Granite 4.0 350M", "provider": "IBM", "intelligence": 8, "params": "0.35B", "dataset": "Granite training dataset"},
    {"name": "Arctic Instruct", "provider": "Snowflake", "intelligence": 8, "params": "480B (17B active)", "dataset": "Arctic training dataset"},
    {"name": "Qwen Chat 72B", "provider": "Alibaba", "intelligence": 8, "params": "72B", "dataset": "Qwen training dataset"},
    {"name": "Command-R+ (Aug '24)", "provider": "Cohere", "intelligence": 7, "params": "104B", "dataset": "Cohere training dataset"},
    {"name": "Llama 3 Instruct 8B", "provider": "Meta", "intelligence": 7, "params": "8B", "dataset": "Llama 3 training dataset"},
    {"name": "Gemma 3 1B Instruct", "provider": "Google", "intelligence": 7, "params": "1B", "dataset": "Gemma 3 training dataset"},
    {"name": "DeepSeek Coder V2 Lite Instruct", "provider": "DeepSeek", "intelligence": 6, "params": "16B (2.4B active)", "dataset": "DeepSeek Coder training dataset"},
    {"name": "Codestral (May '24)", "provider": "Mistral", "intelligence": 6, "params": "22B", "dataset": "Mistral training dataset"},
    {"name": "Gemma 3 270M", "provider": "Google", "intelligence": 6, "params": "0.268B", "dataset": "Gemma 3 training dataset"},
    {"name": "Llama 2 Chat 70B", "provider": "Meta", "intelligence": 6, "params": "70B", "dataset": "Llama 2 training dataset"},
    {"name": "DeepSeek LLM 67B Chat (V1)", "provider": "DeepSeek", "intelligence": 6, "params": "7B", "dataset": "DeepSeek training dataset"},
    {"name": "Llama 2 Chat 13B", "provider": "Meta", "intelligence": 6, "params": "13B", "dataset": "Llama 2 training dataset"},
    {"name": "Command-R+ (Apr '24)", "provider": "Cohere", "intelligence": 5, "params": "104B", "dataset": "Cohere training dataset"},
    {"name": "OpenChat 3.5 (1210)", "provider": "OpenChat", "intelligence": 5, "params": "7B", "dataset": "OpenChat training dataset"},
    {"name": "DBRX Instruct", "provider": "Databricks", "intelligence": 5, "params": "132B (36B active)", "dataset": "DBRX training dataset"},
    {"name": "Mistral NeMo", "provider": "Mistral", "intelligence": 5, "params": "12B", "dataset": "Mistral training dataset"},
    {"name": "Jamba 1.5 Mini", "provider": "AI21 Labs", "intelligence": 4, "params": "52B (12B active)", "dataset": "Jamba training dataset"},
    {"name": "Jamba 1.6 Mini", "provider": "AI21 Labs", "intelligence": 3, "params": "52B (12B active)", "dataset": "Jamba training dataset"},
    {"name": "Mixtral 8x7B Instruct", "provider": "Mistral", "intelligence": 3, "params": "46.7B (12.9B active)", "dataset": "Mixtral training dataset"},
    {"name": "DeepHermes 3 - Llama-3.1 8B Preview (Non-reasoning)", "provider": "Nous Research", "intelligence": 2, "params": "8B", "dataset": "DeepHermes training dataset"},
    {"name": "Llama 65B", "provider": "Meta", "intelligence": 1, "params": "65B", "dataset": "Llama training dataset"},
    {"name": "Qwen Chat 14B", "provider": "Alibaba", "intelligence": 1, "params": "14B", "dataset": "Qwen training dataset"},
    {"name": "Codestral-Mamba", "provider": "Mistral", "intelligence": 1, "params": "7B", "dataset": "Mistral training dataset"},
    {"name": "Mistral 7B Instruct", "provider": "Mistral", "intelligence": 1, "params": "7B", "dataset": "Mistral training dataset"},
    {"name": "Command-R (Aug '24)", "provider": "Cohere", "intelligence": 1, "params": "32B", "dataset": "Cohere training dataset"},
    {"name": "Command-R (Mar '24)", "provider": "Cohere", "intelligence": 1, "params": "35B", "dataset": "Cohere training dataset"},
    {"name": "DeepSeek-OCR", "provider": "DeepSeek", "intelligence": None, "params": "3.34B", "dataset": "DeepSeek OCR training dataset"},
    {"name": "Kimi Linear 48B A3B Instruct", "provider": "Moonshot AI", "intelligence": None, "params": "49.1B (3.0B active)", "dataset": "Kimi training dataset"},
    {"name": "Cogito v2.1 (Reasoning)", "provider": "Deep Cogito", "intelligence": None, "params": "671B", "dataset": "Cogito training dataset"},
]

def generate_scores_from_intelligence(intelligence_score: int) -> Dict[str, float]:
    """Generate benchmark scores based on intelligence score"""
    if intelligence_score is None:
        return {}
    
    # Convert intelligence score (0-100) to base score (0-1)
    base_score = intelligence_score / 100.0
    
    # Create realistic score distribution across benchmarks
    # Higher intelligence = better scores across all benchmarks
    scores = {
        "mmlu": min(0.95, base_score + 0.15),
        "aalcr": min(0.90, base_score + 0.10),
        "scicode": min(0.85, base_score * 0.6),  # SciCode is typically lower
        "tau2-bench": min(0.90, base_score + 0.08),
        "telecom": min(0.88, base_score + 0.06),
        "hellaswag": min(0.92, base_score + 0.12),
        "arc": min(0.90, base_score + 0.10),
        "truthfulqa": min(0.88, base_score + 0.08),
        "gsm8k": min(0.93, base_score + 0.13),
        "winogrande": min(0.91, base_score + 0.11),
    }
    
    # Add some variation
    import random
    random.seed(hash(str(intelligence_score)) % 1000)
    for key in scores:
        variation = (random.random() - 0.5) * 0.05
        scores[key] = max(0.0, min(1.0, scores[key] + variation))
    
    return scores

def create_model_entry(model_data: Dict) -> Dict:
    """Create a model entry for the evaluations data"""
    model_id = model_data["name"].lower().replace(" ", "-").replace("'", "").replace("(", "").replace(")", "").replace(".", "-")
    model_id = "".join(c for c in model_id if c.isalnum() or c == "-")
    
    intelligence = model_data.get("intelligence")
    scores = generate_scores_from_intelligence(intelligence) if intelligence else {}
    
    return {
        "id": model_id,
        "name": model_data["name"],
        "provider": model_data["provider"],
        "dataset": model_data["dataset"],
        "scores": scores
    }

def main():
    # Load existing benchmarks
    benchmarks = [
        {"id": "mmlu", "name": "MMLU", "full_name": "Massive Multitask Language Understanding"},
        {"id": "aalcr", "name": "AALCR", "full_name": "AALCR Benchmark"},
        {"id": "scicode", "name": "SciCode", "full_name": "Scientific Code Understanding"},
        {"id": "tau2-bench", "name": "τ²-Bench", "full_name": "Tau Squared Benchmark"},
        {"id": "telecom", "name": "Telecom", "full_name": "Telecom Benchmark"},
        {"id": "hellaswag", "name": "HellaSwag", "full_name": "HellaSwag Benchmark"},
        {"id": "arc", "name": "ARC", "full_name": "AI2 Reasoning Challenge"},
        {"id": "truthfulqa", "name": "TruthfulQA", "full_name": "TruthfulQA Benchmark"},
        {"id": "gsm8k", "name": "GSM8K", "full_name": "Grade School Math 8K"},
        {"id": "winogrande", "name": "Winogrande", "full_name": "Winogrande Benchmark"},
    ]
    
    # Create all models
    models = [create_model_entry(model_data) for model_data in MODELS_DATA]
    
    # Create final data structure
    data = {
        "benchmarks": benchmarks,
        "models": models
    }
    
    # Save to file
    with open("evaluations_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Added {len(models)} models to evaluations_data.json")
    print(f"✓ Benchmarks: {len(benchmarks)}")
    print(f"\nNote: Scores are generated based on Intelligence scores.")
    print("To get actual benchmark scores, please fetch from the API or update manually.")

if __name__ == "__main__":
    main()




