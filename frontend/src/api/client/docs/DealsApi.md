# DealsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**createDealApiV1DealsPost**](#createdealapiv1dealspost) | **POST** /api/v1/deals/ | Create Deal|

# **createDealApiV1DealsPost**
> DealResponseDTO createDealApiV1DealsPost(dealCreateRequestDTO)

Create a deal

### Example

```typescript
import {
    DealsApi,
    Configuration,
    DealCreateRequestDTO
} from './api';

const configuration = new Configuration();
const apiInstance = new DealsApi(configuration);

let dealCreateRequestDTO: DealCreateRequestDTO; //

const { status, data } = await apiInstance.createDealApiV1DealsPost(
    dealCreateRequestDTO
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **dealCreateRequestDTO** | **DealCreateRequestDTO**|  | |


### Return type

**DealResponseDTO**

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Deal created successfully |  -  |
|**400** | Validation error |  -  |
|**401** | Authentication required |  -  |
|**403** | Cannot create deal for own advert |  -  |
|**404** | Advert not found |  -  |
|**409** | Deal already exists |  -  |
|**422** | Validation Error |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

