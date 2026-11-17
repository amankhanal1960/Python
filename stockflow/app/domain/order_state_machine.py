import enum


class OrderStatus(str, enum.Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    REFUNDED = "REFUNDED"


VALID_ORDER_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING_PAYMENT: {
        OrderStatus.PAID,
        OrderStatus.EXPIRED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.PAID: {
        OrderStatus.COMPLETED,
        OrderStatus.REFUNDED,
    },
    OrderStatus.COMPLETED: {
        OrderStatus.REFUNDED,
    },
    OrderStatus.EXPIRED: set(),
    OrderStatus.CANCELLED: set(),
    OrderStatus.REFUNDED: set(),
}


class InvalidOrderTransitionError(Exception):
    pass


def validate_and_get_next_status(current_status: str, next_status: OrderStatus) -> str:
    current = OrderStatus(current_status)
    if next_status not in VALID_ORDER_TRANSITIONS[current]:
        raise InvalidOrderTransitionError(
            f"Cannot change order status from {current.value}"
        )
    return next_status.value
