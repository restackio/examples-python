from restack_ai.function import function, log
from pydantic import BaseModel

class LookupSalesInput(BaseModel):
    category: str

class SalesItem(BaseModel):
    item_id: int
    type: str
    name: str
    retail_price_usd: float
    sale_price_usd: float
    sale_discount_pct: int

class SalesInput(BaseModel):
    category: str

@function.defn()
async def lookupSales(input: LookupSalesInput) -> str:
    try:
        log.info("lookupSales function started", input=input)
        
        items = [
            SalesItem(item_id=101, type="snowboard", name="Alpine Blade", retail_price_usd=450, sale_price_usd=360, sale_discount_pct=20),
            SalesItem(item_id=102, type="snowboard", name="Peak Bomber", retail_price_usd=499, sale_price_usd=374, sale_discount_pct=25),
            SalesItem(item_id=201, type="apparel", name="Thermal Jacket", retail_price_usd=120, sale_price_usd=84, sale_discount_pct=30),
            SalesItem(item_id=202, type="apparel", name="Insulated Pants", retail_price_usd=150, sale_price_usd=112, sale_discount_pct=25),
            SalesItem(item_id=301, type="boots", name="Glacier Grip", retail_price_usd=250, sale_price_usd=200, sale_discount_pct=20),
            SalesItem(item_id=302, type="boots", name="Summit Steps", retail_price_usd=300, sale_price_usd=210, sale_discount_pct=30),
            SalesItem(item_id=401, type="accessories", name="Goggles", retail_price_usd=80, sale_price_usd=60, sale_discount_pct=25),
            SalesItem(item_id=402, type="accessories", name="Warm Gloves", retail_price_usd=60, sale_price_usd=48, sale_discount_pct=20),
        ]

        if input.category == "any":
            filtered_items = items
        else:
            filtered_items = [item for item in items if item.type == input.category]

        # Sort by largest discount first
        filtered_items.sort(key=lambda x: x.sale_discount_pct, reverse=True)

        return {"sales": filtered_items}
    except Exception as e:
        log.error("lookupSales function failed", error=e)
        raise e
