from base.constants import BaseConstant


class EventStatus(BaseConstant):
    Created = "created"
    Canceled = "canceled"
    OnGoing = "ongoing"
    Completed = "completed"


class EventAttendanceIntent(BaseConstant):
    Reserved = "Reserved"
    Canceled = "Canceled"


class EventSaveAction(BaseConstant):
    Saved = "Saved"
    Removed = "Removed"
