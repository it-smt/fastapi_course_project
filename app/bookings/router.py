from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBooking]:
    bookings = await BookingDAO.find_all(user_id=user.id)
    booking_dict = parse_obj_as(SBooking, bookings[0]).dict()
    print(booking_dict)
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return bookings


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    await BookingDAO.add(user.id, room_id, date_from, date_to)
