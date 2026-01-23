# AdvertsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**createAdvertApiV1AdvertsPost**](#createadvertapiv1advertspost) | **POST** /api/v1/adverts/ | Create Advert|
|[**deleteAdvertApiV1AdvertsAdvertIdDelete**](#deleteadvertapiv1advertsadvertiddelete) | **DELETE** /api/v1/adverts/{advert_id} | Delete Advert|
|[**getAdvertApiV1AdvertsAdvertIdGet**](#getadvertapiv1advertsadvertidget) | **GET** /api/v1/adverts/{advert_id} | Get Advert|
|[**getAllAdvertsApiV1AdvertsGet**](#getalladvertsapiv1advertsget) | **GET** /api/v1/adverts/ | Get All Adverts|
|[**getInDealsAdvertsApiV1AdvertsDealsGet**](#getindealsadvertsapiv1advertsdealsget) | **GET** /api/v1/adverts/deals | Get In Deals Adverts|
|[**getLikedAdvertsApiV1AdvertsLikedGet**](#getlikedadvertsapiv1advertslikedget) | **GET** /api/v1/adverts/liked | Get Liked Adverts|
|[**getMyAdvertsApiV1AdvertsCreatedGet**](#getmyadvertsapiv1advertscreatedget) | **GET** /api/v1/adverts/created | Get My Adverts|
|[**getSearchAdvertsApiV1AdvertsSearchPost**](#getsearchadvertsapiv1advertssearchpost) | **POST** /api/v1/adverts/search | Get Search Adverts|
|[**updateAdvertFullApiV1AdvertsAdvertIdPut**](#updateadvertfullapiv1advertsadvertidput) | **PUT** /api/v1/adverts/{advert_id} | Update Advert Full|
|[**updateAdvertPartialApiV1AdvertsAdvertIdPatch**](#updateadvertpartialapiv1advertsadvertidpatch) | **PATCH** /api/v1/adverts/{advert_id} | Update Advert Partial|

# **createAdvertApiV1AdvertsPost**
> AdvertResponseDTO createAdvertApiV1AdvertsPost(advertCreateDTO)


### Example

```typescript
import {
    AdvertsApi,
    Configuration,
    AdvertCreateDTO
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

let advertCreateDTO: AdvertCreateDTO; //

const { status, data } = await apiInstance.createAdvertApiV1AdvertsPost(
    advertCreateDTO
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **advertCreateDTO** | **AdvertCreateDTO**|  | |


### Return type

**AdvertResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deleteAdvertApiV1AdvertsAdvertIdDelete**
> deleteAdvertApiV1AdvertsAdvertIdDelete()

Delete advert - только для владельца

### Example

```typescript
import {
    AdvertsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

let advertId: string; // (default to undefined)

const { status, data } = await apiInstance.deleteAdvertApiV1AdvertsAdvertIdDelete(
    advertId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **advertId** | [**string**] |  | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getAdvertApiV1AdvertsAdvertIdGet**
> AdvertResponseDTO getAdvertApiV1AdvertsAdvertIdGet()

Get advert by ID

### Example

```typescript
import {
    AdvertsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

let advertId: string; // (default to undefined)

const { status, data } = await apiInstance.getAdvertApiV1AdvertsAdvertIdGet(
    advertId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **advertId** | [**string**] |  | defaults to undefined|


### Return type

**AdvertResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getAllAdvertsApiV1AdvertsGet**
> AdvertListResponseDTO getAllAdvertsApiV1AdvertsGet()

Get all adverts

### Example

```typescript
import {
    AdvertsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

const { status, data } = await apiInstance.getAllAdvertsApiV1AdvertsGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**AdvertListResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**400** | Validation error |  -  |
|**401** | Authentication required |  -  |
|**403** | Not enough permissions |  -  |
|**404** | Advert or category not found |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getInDealsAdvertsApiV1AdvertsDealsGet**
> AdvertListResponseDTO getInDealsAdvertsApiV1AdvertsDealsGet()

Get all adverts in deals

### Example

```typescript
import {
    AdvertsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

const { status, data } = await apiInstance.getInDealsAdvertsApiV1AdvertsDealsGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**AdvertListResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful response |  -  |
|**401** | Authentication required |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getLikedAdvertsApiV1AdvertsLikedGet**
> AdvertListResponseDTO getLikedAdvertsApiV1AdvertsLikedGet()

Get all adverts liked

### Example

```typescript
import {
    AdvertsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

const { status, data } = await apiInstance.getLikedAdvertsApiV1AdvertsLikedGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**AdvertListResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful response |  -  |
|**401** | Authentication required |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getMyAdvertsApiV1AdvertsCreatedGet**
> AdvertListResponseDTO getMyAdvertsApiV1AdvertsCreatedGet()

Get all adverts my created

### Example

```typescript
import {
    AdvertsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

const { status, data } = await apiInstance.getMyAdvertsApiV1AdvertsCreatedGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**AdvertListResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getSearchAdvertsApiV1AdvertsSearchPost**
> AdvertListResponseDTO getSearchAdvertsApiV1AdvertsSearchPost(advertSearchRequestDTO)

Get all adverts

### Example

```typescript
import {
    AdvertsApi,
    Configuration,
    AdvertSearchRequestDTO
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

let advertSearchRequestDTO: AdvertSearchRequestDTO; //

const { status, data } = await apiInstance.getSearchAdvertsApiV1AdvertsSearchPost(
    advertSearchRequestDTO
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **advertSearchRequestDTO** | **AdvertSearchRequestDTO**|  | |


### Return type

**AdvertListResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**400** | Validation error |  -  |
|**401** | Authentication required |  -  |
|**403** | Not enough permissions |  -  |
|**404** | Advert or category not found |  -  |
|**422** | Validation Error |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateAdvertFullApiV1AdvertsAdvertIdPut**
> AdvertResponseDTO updateAdvertFullApiV1AdvertsAdvertIdPut(advertUpdateFullDTO)

Update advert (full update) - только для владельца

### Example

```typescript
import {
    AdvertsApi,
    Configuration,
    AdvertUpdateFullDTO
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

let advertId: string; // (default to undefined)
let advertUpdateFullDTO: AdvertUpdateFullDTO; //

const { status, data } = await apiInstance.updateAdvertFullApiV1AdvertsAdvertIdPut(
    advertId,
    advertUpdateFullDTO
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **advertUpdateFullDTO** | **AdvertUpdateFullDTO**|  | |
| **advertId** | [**string**] |  | defaults to undefined|


### Return type

**AdvertResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updateAdvertPartialApiV1AdvertsAdvertIdPatch**
> AdvertResponseDTO updateAdvertPartialApiV1AdvertsAdvertIdPatch(advertUpdatePartialDTO)

Update advert (partial update) - только для владельца

### Example

```typescript
import {
    AdvertsApi,
    Configuration,
    AdvertUpdatePartialDTO
} from './api';

const configuration = new Configuration();
const apiInstance = new AdvertsApi(configuration);

let advertId: string; // (default to undefined)
let advertUpdatePartialDTO: AdvertUpdatePartialDTO; //

const { status, data } = await apiInstance.updateAdvertPartialApiV1AdvertsAdvertIdPatch(
    advertId,
    advertUpdatePartialDTO
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **advertUpdatePartialDTO** | **AdvertUpdatePartialDTO**|  | |
| **advertId** | [**string**] |  | defaults to undefined|


### Return type

**AdvertResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

