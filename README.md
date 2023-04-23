<h1 align="center">Steeleye Backend Assessment 📝</h1>

<details>
<summary>Task</summary>
<br>

# Table of Contents

1.  [Introduction](#intro)
    1.  [Constraints](#constraints)
    1.  [Database](#database)
        1.  [Schema Model](#schemamodel)
1.  [Test](#test)
    1.  [Listing trades](#listingtrades)
    1.  [Single trade](#singletrade)
    1.  [Searching trades](#searchingtrades)
    1.  [Advanced filtering](#advancedfiltering)
    1.  [Bonus points](#bonus)
1. [Submission](#submission)
1. [Resources](#resources)


<a id="intro"></a>

# Introduction

At SteelEye we are using [FastAPI](https://fastapi.tiangolo.com/) for our primary client-facing API layer. 
FastAPI's usage of [Pydantic](https://pydantic-docs.helpmanual.io/) for expressing data types aligns quite well 
with how we model our own Schema models (using Pydantic).

In this exercise, you will be building a _REST_ API with endpoints serving Trade
data from a mocked database.

<a id="constraints"></a>

## Constraints

You are expected to write the API in Python using the FastAPI framework. You are
not expected to have any previous FastAPI experience and unfamiliarty with FastAPI will not be held against you when reviewing your submission. However, it is expected that you will be able to produce a functional API.

<a id="database"></a>

## Database

At SteelEye we use Elasticsearch as our primary data storage technology. Setting up an instance of Elasticsearch with the necessary mappings and data required for the functionality in this test is outside of the scope of submission.

We _do_ expect you to mock a database interaction layer in any way you see fit and generate data (which can be randomized) for the purposes of this test. The implementation of this database layer is left up to you.

<a id="schemamodel"></a>

### Schema model

We have provided a Pydantic model representing a single Trade below:

```python
import datetime as dt

from typing import Optional
from pydantic import BaseModel, Field

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

```

<a id="test"></a>

# Test

This tests represents a common request when building an API. You need to provide a set of endpoints for retrieving a list of Trades, retrieving a single Trade by ID, searching against Trades, and filtering Trades


<a id="listingtrades"></a>

## Listing trades

Please provide an endpoint to fetch a list of trades.

<a id="singletrade"></a>

## Single trade

Users would like to be able to retrieve a single trade from the API. Please provide an endpoint to fetch a trade by id.

<a id="searchingtrades"></a>

## Searching trades

Users would now like to be able to search across the trades using the API. Your endpoint for fetching a list of trades will need to support searching for trades through the following fields:

- `counterparty`
- `instrumentId`
- `instrumentName`
- `trader`

If a user was to call your endpoint and provide a `?search=bob%20smith` query parameter, your endpoint will return any trades where the text `bob smith` exists in any of the fields listed above.

<a id="advancedfiltering"></a>

## Advanced filtering

The users would now like the ability to filter trades. Your endpoint for fetching a list of trades will need to support filtering using the following optional query parameters:

| Parameter | Description |
|-----------|-------------|
|`assetClass`|Asset class of the trade.|
|`end`|The maximum date for the `tradeDateTime` field.|
|`maxPrice`|The maximum value for the `tradeDetails.price` field.|
|`minPrice`|The minimum value for the `tradeDetails.price` field.|
|`start`|The minimum date for the `tradeDateTime` field.|
|`tradeType`|The `tradeDetails.buySellIndicator` is a `BUY` or `SELL`|
|||

All maximum and minimum fields are inclusive (e.g. `minPrice=2&maxPrice=10` will
return `2 <= tradeDetails.price <= 10`).

<a id="bonus"></a>

## Bonus points

Implement support for pagination and sorting on the list of trades.

<a id="submission"></a>

## Submission

You can return your solution via email, or provide access to a Git repo. Please include a document describing your solution and the reasoning behind your approach. Incomplete solutions will not be considered.

<a id="resources"></a>

## Resources
- FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- Pydantic: [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)
</details>

<hr>

<details open>
<summary>Solution</summary>
<br>

### Tech Stack:

<ol>
  <li> Python </li>
  <li> FastAPI </li>
  <li> Uvicorn </li>
  <li> ElasticSearch </li>
  <li> Render </li>
</ol>

<br>

### API link : [FastAPI - Swagger UI](https://fast-api-gcci.onrender.com/docs)

### Documentation: [Doc Link](https://github.com/SomyaRanjanSahu/Steeleye_Backend/blob/main/Documentation.pdf)

<br>

### Swagger UI preview:

<img src="https://i.postimg.cc/sg5LTrxY/ui.png" alt = "Swagger UI preview">

</details>
