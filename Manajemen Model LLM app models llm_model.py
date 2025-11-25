import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.config.settings import get_settings
import asyncio
from functools import lru_cache

settings = get_settings()
model = None
tokenizer = None

async def get_model():
    """Load model once and cache it[citation:9]"""
    global model, tokenizer
    
    if model is None:
        # Load base model (contoh dengan Mistral)
        tokenizer = AutoTokenizer.from_pretrained(
            settings.model_name,
            use_fast=True
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            settings.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer

async def predict(request):
    """Async prediction function"""
    model, tokenizer = await get_model()
    
    # Encode input
    inputs = tokenizer(
        request.prompt,
        return_tensors="pt",
        truncation=True,
        max_length=request.max_length
    ).to(model.device)
    
    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    generated_text = tokenizer.decode(
        outputs[0], 
        skip_special_tokens=True
    )
    
    return generated_text