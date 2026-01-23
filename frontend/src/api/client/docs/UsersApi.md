# UsersApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**getCurrentUserProfileApiV1UsersMeGet**](#getcurrentuserprofileapiv1usersmeget) | **GET** /api/v1/users/me | Get Current User Profile|
|[**loginUserApiV1UsersLoginPost**](#loginuserapiv1usersloginpost) | **POST** /api/v1/users/login | Login User|
|[**logoutUserApiV1UsersLogoutPost**](#logoutuserapiv1userslogoutpost) | **POST** /api/v1/users/logout | Logout User|
|[**registerUserApiV1UsersRegisterPost**](#registeruserapiv1usersregisterpost) | **POST** /api/v1/users/register | Register User|

# **getCurrentUserProfileApiV1UsersMeGet**
> UserResponse getCurrentUserProfileApiV1UsersMeGet()


### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

const { status, data } = await apiInstance.getCurrentUserProfileApiV1UsersMeGet();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**UserResponse**

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

# **loginUserApiV1UsersLoginPost**
> TokenResponse loginUserApiV1UsersLoginPost(userLogin)

User login

### Example

```typescript
import {
    UsersApi,
    Configuration,
    UserLogin
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let userLogin: UserLogin; //

const { status, data } = await apiInstance.loginUserApiV1UsersLoginPost(
    userLogin
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userLogin** | **UserLogin**|  | |


### Return type

**TokenResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logoutUserApiV1UsersLogoutPost**
> SuccessResponse logoutUserApiV1UsersLogoutPost()

User logout

### Example

```typescript
import {
    UsersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

const { status, data } = await apiInstance.logoutUserApiV1UsersLogoutPost();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**SuccessResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **registerUserApiV1UsersRegisterPost**
> UserResponse registerUserApiV1UsersRegisterPost(userRegister)

Register new user

### Example

```typescript
import {
    UsersApi,
    Configuration,
    UserRegister
} from './api';

const configuration = new Configuration();
const apiInstance = new UsersApi(configuration);

let userRegister: UserRegister; //

const { status, data } = await apiInstance.registerUserApiV1UsersRegisterPost(
    userRegister
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userRegister** | **UserRegister**|  | |


### Return type

**UserResponse**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** | Successful Response |  -  |
|**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

