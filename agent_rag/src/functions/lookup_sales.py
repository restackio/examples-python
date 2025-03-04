from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log


class SalesItem(BaseModel):
    item_id: int
    type: str
    name: str
    retail_price_usd: float
    sale_price_usd: float
    sale_discount_pct: int


@function.defn()
async def lookup_sales() -> str:
    try:
        log.info("lookup_sales function started")

        items = [
            SalesItem(
                item_id=101,
                type="snowboard",
                name="Alpine Blade",
                retail_price_usd=450,
                sale_price_usd=360,
                sale_discount_pct=20,
            ),
            SalesItem(
                item_id=102,
                type="snowboard",
                name="Peak Bomber",
                retail_price_usd=499,
                sale_price_usd=374,
                sale_discount_pct=25,
            ),
            SalesItem(
                item_id=201,
                type="apparel",
                name="Thermal Jacket",
                retail_price_usd=120,
                sale_price_usd=84,
                sale_discount_pct=30,
            ),
            SalesItem(
                item_id=202,
                type="apparel",
                name="Insulated Pants",
                retail_price_usd=150,
                sale_price_usd=112,
                sale_discount_pct=25,
            ),
            SalesItem(
                item_id=301,
                type="boots",
                name="Glacier Grip",
                retail_price_usd=250,
                sale_price_usd=200,
                sale_discount_pct=20,
            ),
            SalesItem(
                item_id=302,
                type="boots",
                name="Summit Steps",
                retail_price_usd=300,
                sale_price_usd=210,
                sale_discount_pct=30,
            ),
            SalesItem(
                item_id=401,
                type="accessories",
                name="Goggles",
                retail_price_usd=80,
                sale_price_usd=60,
                sale_discount_pct=25,
            ),
            SalesItem(
                item_id=402,
                type="accessories",
                name="Warm Gloves",
                retail_price_usd=60,
                sale_price_usd=48,
                sale_discount_pct=20,
            ),
        ]

        return str(items)
    except Exception as e:
        error_message = f"lookup_sales function failed: {e}"
        raise NonRetryableError(error_message) from e
