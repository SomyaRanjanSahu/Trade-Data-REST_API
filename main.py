import datetime as dt
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query

app = FastAPI()

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")

class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")

class MockDB:
    def __init__(self):
        self.trades = []

    def add_trade(self, trade: Trade):
        self.trades.append(trade)

    def get_trade_by_id(self, trade_id: str) -> Trade:
        for trade in self.trades:
            if trade.trade_id == trade_id:
                return trade
        return None

    def search_trades(self, search_str: str) -> List[Trade]:
        results = []
        for trade in self.trades:
            if search_str.lower() in str(trade).lower():
                results.append(trade)
        return results

    def filter_trades(self, asset_class: str = None, start: dt.datetime = None, end: dt.datetime = None, 
                      trade_type: str = None, min_price: float = None, max_price: float = None) -> List[Trade]:
        results = self.trades
        if asset_class:
            results = [trade for trade in results if trade.asset_class == asset_class]
        if start:
            results = [trade for trade in results if trade.trade_date_time >= start]
        if end:
            results = [trade for trade in results if trade.trade_date_time <= end]
        if trade_type:
            results = [trade for trade in results if trade.trade_details.buySellIndicator == trade_type]
        if min_price:
            results = [trade for trade in results if trade.trade_details.price >= min_price]
        if max_price:
            results = [trade for trade in results if trade.trade_details.price <= max_price]
        return results

    def update_trade(self, trade_id: str, trade: Trade):
        for i in range(len(self.trades)):
            if self.trades[i].trade_id == trade_id:
                self.trades[i] = trade
                return True
        return False

    def delete_trade(self, trade_id: str):
        for i in range(len(self.trades)):
            if self.trades[i].trade_id == trade_id:
                del self.trades[i]
                return True
        return False

db = MockDB()

@app.post("/trades")
async def create_trade(trade: Trade):
    db.add_trade(trade)
    return {"status": "success", "msg": "Trade added successfully"}

@app.get("/trades/{trade_id}")
async def get_trade(trade_id: str):
    trade = db.get_trade_by_id(trade_id)
    if trade:
        return trade
    else:
        return {"status": "failure", "msg": "Trade not found"}

@app.get("/trades")
async def search_trades(asset_class: Optional[str] = None,
                        start: Optional[dt.datetime] = None,
                        end: Optional[dt.datetime] = None,
                        trade_type: Optional[str] = None,
                        min_price: Optional[float] = None,
                        max_price: Optional[float] = None,
                        skip: int = 0,
                        limit: int = 100,
                        sort: Optional[str] = None):
    results = db.filter_trades(asset_class=asset_class, start=start, end=end, trade_type=trade_type, 
                               min_price=min_price, max_price=max_price)

    total = len(results)
    page = results[skip: skip + limit]

    if sort:
        field, order = sort.split(":")
        reverse = False if order == "asc" else True
        page = sorted(page, key=lambda trade: getattr(trade, field), reverse=reverse)

    return {"total": total, "page": page, "skip": skip, "limit": limit}

@app.get("/trades/filter")
async def filter_trades(asset_class: Optional[str] = None, start: Optional[dt.datetime] = None, 
                        end: Optional[dt.datetime] = None, trade_type: Optional[str] = None, 
                        min_price: Optional[float] = None, max_price: Optional[float] = None):
    trades = db.filter_trades(asset_class=asset_class, start=start, end=end, trade_type=trade_type, 
                              min_price=min_price, max_price=max_price)
    if trades:
        return trades
    else:
        return {"status": "failure", "msg": "No trades found"}

@app.put("/trades/{trade_id}")
async def update_trade(trade_id: str, trade: Trade):
    if db.update_trade(trade_id, trade):
        return {"status": "success", "msg": "Trade updated successfully"}
    else:
        return {"status": "failure", "msg": "Trade not found"}

@app.delete("/trades/{trade_id}")
async def delete_trade(trade_id: str):
    if db.delete_trade(trade_id):
        return {"status": "success", "msg": "Trade deleted successfully"}
    else:
        return {"status": "failure", "msg": "Trade not found"}