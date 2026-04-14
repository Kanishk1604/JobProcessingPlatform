
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(tags=["answer"])

@router.get("/answer")
def sum():
    res = 1+2
    return {
       3
    }