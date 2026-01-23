# CategoriesApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**getAllCategoriesApiV1CategoriesGet**](#getallcategoriesapiv1categoriesget) | **GET** /api/v1/categories/ | Get All Categories|
|[**getCategoryApiV1CategoriesCategoryIdGet**](#getcategoryapiv1categoriescategoryidget) | **GET** /api/v1/categories/{category_id} | Get Category|

# **getAllCategoriesApiV1CategoriesGet**
> CategoryListResponseDTO getAllCategoriesApiV1CategoriesGet()

Get all categories

### Example

```typescript
import {
    CategoriesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CategoriesApi(configuration);

const { status, data } = await apiInstance.getAllCategoriesApiV1CategoriesGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**CategoryListResponseDTO**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful response |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getCategoryApiV1CategoriesCategoryIdGet**
> string getCategoryApiV1CategoriesCategoryIdGet()

Get category by ID

### Example

```typescript
import {
    CategoriesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CategoriesApi(configuration);

let categoryId: string; // (default to undefined)

const { status, data } = await apiInstance.getCategoryApiV1CategoriesCategoryIdGet(
    categoryId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **categoryId** | [**string**] |  | defaults to undefined|


### Return type

**string**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful response |  -  |
|**404** | Category not found |  -  |
|**422** | Validation Error |  -  |
|**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

