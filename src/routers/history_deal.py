from fastapi import APIRouter

router_history = APIRouter()

'''
async def get_controller() -> HistoryDealController:
    # 1. Получаем асинхронную сессию БД
    session = await get_session(role="admin")

    try:
        # 2. Создаем SQL билдер
        builder: IHistoryDealSqlBuilder = HistoryDealSqlBuilder()

        # 3. Создаем репозиторий с сессией и билдером
        repository = HistoryDealRepository(session, builder)

        # 4. Создаем сервис с репозиторием
        service = HistoryDealService(repository)

        # 5. Создаем контроллер с сервисом
        controller = HistoryDealController(service)

        return controller
    finally:
        await session.close()  # закрываем сессию


@router_history.get("/history/all")
async def history_all(request: Request, ctrl: HistoryDealController = Depends(get_controller)):
    print('here')
    return await ctrl.list_all(request)


@router_history.get("/history/my")
async def history_my(request: Request, ctrl: HistoryDealController = Depends(get_controller)):
    return await ctrl.list_user(request)

'''