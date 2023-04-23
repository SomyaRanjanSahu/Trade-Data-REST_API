import datetime as dt
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query

# Created a FastAPI instance
app = FastAPI()

# Defined a Pydantic model for the trade details
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(
        description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")

# Defined a Pydantic model for the trade
class Trade(BaseModel):
    asset_class: Optional[str] = Field(
        alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(
        default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(
        alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(
        alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(
        alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(
        alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None,
                          description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")

# Defined a mock database class to simulate a database for storing trades
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
            results = [
                trade for trade in results if trade.asset_class == asset_class]
        if start:
            results = [
                trade for trade in results if trade.trade_date_time >= start]
        if end:
            results = [
                trade for trade in results if trade.trade_date_time <= end]
        if trade_type:
            results = [
                trade for trade in results if trade.trade_details.buySellIndicator == trade_type]
        if min_price:
            results = [
                trade for trade in results if trade.trade_details.price >= min_price]
        if max_price:
            results = [
                trade for trade in results if trade.trade_details.price <= max_price]
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

# Created an instance of the mock database
mock_db = MockDB()

# Created a POST endpoint for creating trades
@app.post("/trades")
def create_trade(trade: Trade):
    mock_db.add_trade(trade)
    return {"message": "Trade created successfully"}

# Created a GET endpoint for filtering trades
@app.get("/trades")
def filter_trades(asset_class: str = None, start: dt.datetime = None, end: dt.datetime = None,
                  trade_type: str = None, min_price: float = None, max_price: float = None,
                  limit: int = 100, offset: int = 0, sort_by: str = None):
    results = mock_db.filter_trades(asset_class=asset_class, start=start, end=end, trade_type=trade_type,
                                    min_price=min_price, max_price=max_price)
    total_results = len(results)
    if sort_by:
        results = sorted(results, key=lambda x: getattr(x, sort_by))
    results = results[offset:offset+limit]
    return {"total_results": total_results, "trades": results}

# Created a GET endpoint for retrieving trades by ID
@app.get("/trades/{trade_id}")
def get_trade_by_id(trade_id: str):
    trade = mock_db.get_trade_by_id(trade_id)
    if trade:
        return trade
    else:
        return {"error": "Trade not found"}

# Created a GET endpoint for searching trades
@app.get("/trades/search")
async def search_trades(string: Optional[str] = None,
                        counter_party: Optional[str] = None,
                        instrument_id: Optional[str] = None,
                        instrument_name: Optional[str] = None,
                        trader: Optional[str] = None):

    if string:
        results = mock_db.search_trades(string)
        return results
    elif counter_party:
        results = mock_db.search_trades(counter_party)
        return results
    elif instrument_id:
        results = mock_db.search_trades(instrument_id)
        return results
    elif instrument_name:
        results = mock_db.search_trades(instrument_name)
        return results
    elif trader:
        results = mock_db.search_trades(trader)
        return results
    else:
        return {"Trade not found"}
        
# Created a PUT endpoint for updating trades
@app.put("/trades/{trade_id}")
async def update_trade(trade_id: str, trade: Trade):
    if mock_db.update_trade(trade_id, trade):
        return {"status": "success", "msg": "Trade updated successfully"}
    else:
        return {"status": "failure", "msg": "Trade not found"}

# Created a DELETE endpoint for deleting trades
@app.delete("/trades/{trade_id}")
async def delete_trade(trade_id: str):
    if mock_db.delete_trade(trade_id):
        return {"status": "success", "msg": "Trade deleted successfully"}
    else:
        return {"status": "failure", "msg": "Trade not found"}
