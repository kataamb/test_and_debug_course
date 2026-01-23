# LikesApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**addLikeApiV1AdvertsAdvertIdLikesPost**](#addlikeapiv1advertsadvertidlikespost) | **POST** /api/v1/adverts/{advert_id}/likes | Add Like|
|[**removeLikeApiV1AdvertsAdvertIdLikesDelete**](#removelikeapiv1advertsadvertidlikesdelete) | **DELETE** /api/v1/adverts/{advert_id}/likes | Remove Like|

# **addLikeApiV1AdvertsAdvertIdLikesPost**
> LikeResponseDTO addLikeApiV1AdvertsAdvertIdLikesPost()

Like an advert

### Example

```typescript
import {
    LikesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new LikesApi(configuration);

let advertId: string; // (default to undefined)

const { status, data } = await apiInstance.addLikeApiV1AdvertsAdvertIdLikesPost(
    advertId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **advertId** | [**string**] |  | defaults to undefined|


### Return type

**LikeResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Like added successfully |  -  |
|**401** | Authentication required |  -  |
|**403** | Cannot like own advert |  -  |
|**404** | Advert not found |  -  |
|**409** | Like already exists |  -  |
|**422** | Validation Error |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **removeLikeApiV1AdvertsAdvertIdLikesDelete**
> removeLikeApiV1AdvertsAdvertIdLikesDelete()

Remove like from advert

### Example

```typescript
import {
    LikesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new LikesApi(configuration);

let advertId: string; // (default to undefined)

const { status, data } = await apiInstance.removeLikeApiV1AdvertsAdvertIdLikesDelete(
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
|**204** | Like removed successfully |  -  |
|**401** | Authentication required |  -  |
|**404** | Like not found |  -  |
|**422** | Validation Error |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

