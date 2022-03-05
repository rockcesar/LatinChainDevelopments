# LatinChain API

The platform API allows you to read data on the LatinChain Servers related.

## Overview

### Base path:

The latest version of the LatinChain API is available at `latin-chain.com/api`.

### Authorization

You only are going to read info, no authorization required.

## API Reference

### Users

Base path: `/api/get-external-user`.

#### Get an user:

Get information about an user.

```
GET /api/get-external-user/{pi_user_code}
```

* Response type: [UserDTO](#UserDTO)

* In case the user doesn't exists, the response is type: [FailDTO](#FailDTO)

## Resource types

### `UserDTO`

```typescript
{
"result": boolean, 
"pi_user_code": string,
"points": float,
"points_chess": float, 
"points_sudoku": float,
"points_snake": float,
"unblocked": boolean
}
```

### `FailDTO`

```typescript
{
"result": boolean
}
```
