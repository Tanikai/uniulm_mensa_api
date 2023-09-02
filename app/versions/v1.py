from typing import Annotated, Any
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from ..dependencies.mensaparser import MensaParser, get_mensa_parser

router = APIRouter()

@router.get("/canteens/{mensa_id}/days/{mensa_date}/meals")
def return_mensaplan(mensa_id: str, mensa_date: str, mensa_parser: Annotated[MensaParser, Depends(get_mensa_parser)]):
    formatted = mensa_parser.get_plan()
    try:
        day_plan = formatted[mensa_id][mensa_date]
        return day_plan
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Could not find plan for {mensa_id} on date {mensa_date}")


@router.get("/canteens/{mensa_id}")
def return_next_plan(mensa_id: str, mensa_parser: Annotated[MensaParser, Depends(get_mensa_parser)]):
    formatted = mensa_parser.get_plan()

    day = date.today()
    found = False
    try:
        mensa = formatted[mensa_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Could not find mensa {mensa_id}")

    date_key = ""
    while not found:
        date_key = day.strftime("%Y-%m-%d")
        if date_key not in mensa:
            day = day + timedelta(days=1)
            continue

        day_plan = mensa[date_key]
        if len(day_plan) > 0:
            found = True
        else:
            day = day + timedelta(days=1)

    redirect_url = router.url_path_for("return_mensaplan", mensa_id=mensa_id, mensa_date=date_key)
    return RedirectResponse(url=redirect_url)


@router.get("/canteens/{mensa_id}/all")
def return_all(mensa_id: str, mensa_parser: Annotated[Any, Depends(get_mensa_parser)]):
    formatted = mensa_parser.get_plan()
    # FIXME: filter by mensa id
    return formatted


@router.get("/mensaplan.json")
def return_fs_et(mensa_parser: Annotated[Any, Depends(get_mensa_parser)]):
    return mensa_parser.get_fs_plan()
