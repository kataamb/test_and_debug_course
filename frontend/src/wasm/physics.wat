(module
  ;; Память для обмена данными
  (memory (export "memory") 1)
  
  ;; Функция обновления позиции шарика
  ;; Возвращает результаты через память
  (func $updateBall (export "updateBall")
    (param $ptr i32)           ;; Указатель на массив [x, y, vx, vy]
    (param $width f32)
    (param $height f32)
    (param $radius f32)
    (param $dt f32)
    
    (local $x f32)
    (local $y f32)
    (local $vx f32)
    (local $vy f32)
    (local $new_x f32)
    (local $new_y f32)
    (local $new_vx f32)
    (local $new_vy f32)
    
    ;; Загружаем данные из памяти
    (local.set $x (f32.load (local.get $ptr)))
    (local.set $y (f32.load offset=4 (local.get $ptr)))
    (local.set $vx (f32.load offset=8 (local.get $ptr)))
    (local.set $vy (f32.load offset=12 (local.get $ptr)))
    
    ;; Новые координаты
    (local.set $new_x
      (f32.add
        (local.get $x)
        (f32.mul (local.get $vx) (local.get $dt))
      )
    )
    
    (local.set $new_y
      (f32.add
        (local.get $y)
        (f32.mul
          (f32.add (local.get $vy) (f32.const 0.5)) ;; Гравитация
          (local.get $dt)
        )
      )
    )
    
    ;; Сохраняем скорости
    (local.set $new_vx (local.get $vx))
    (local.set $new_vy (local.get $vy))
    
    ;; Проверка столкновений с границами
    
    ;; Правая стенка
    (if (f32.gt
          (f32.add (local.get $new_x) (local.get $radius))
          (local.get $width)
        )
      (then
        (local.set $new_vx
          (f32.mul (local.get $vx) (f32.const -0.9))
        )
        (local.set $new_x
          (f32.sub (local.get $width) (local.get $radius))
        )
      )
    )
    
    ;; Левая стенка
    (if (f32.lt
          (f32.sub (local.get $new_x) (local.get $radius))
          (f32.const 0)
        )
      (then
        (local.set $new_vx
          (f32.mul (local.get $vx) (f32.const -0.9))
        )
        (local.set $new_x (local.get $radius))
      )
    )
    
    ;; Нижняя стенка
    (if (f32.gt
          (f32.add (local.get $new_y) (local.get $radius))
          (local.get $height)
        )
      (then
        (local.set $new_vy
          (f32.mul (local.get $vy) (f32.const -0.9))
        )
        (local.set $new_y
          (f32.sub (local.get $height) (local.get $radius))
        )
      )
    )
    
    ;; Верхняя стенка
    (if (f32.lt
          (f32.sub (local.get $new_y) (local.get $radius))
          (f32.const 0)
        )
      (then
        (local.set $new_vy
          (f32.mul (local.get $vy) (f32.const -0.9))
        )
        (local.set $new_y (local.get $radius))
      )
    )
    
    ;; Сохраняем результаты обратно в память
    (f32.store (local.get $ptr) (local.get $new_x))
    (f32.store offset=4 (local.get $ptr) (local.get $new_y))
    (f32.store offset=8 (local.get $ptr) (local.get $new_vx))
    (f32.store offset=12 (local.get $ptr) (local.get $new_vy))
  )
  
  ;; Функция обновления массива шариков
  (func $updateBalls (export "updateBalls")
    (param $ptr i32)           ;; Указатель на массив шариков
    (param $count i32)         ;; Количество шариков
    (param $width f32)
    (param $height f32)
    (param $radius f32)
    (param $dt f32)
    
    (local $i i32)
    (local $current_ptr i32)
    
    (local.set $i (i32.const 0))
    
    (loop $loop
      ;; Вычисляем указатель на текущий шарик (каждый шарик = 4 float * 4 bytes = 16 bytes)
      (local.set $current_ptr
        (i32.add
          (local.get $ptr)
          (i32.mul (local.get $i) (i32.const 16))
        )
      )
      
      ;; Обновляем шарик
      (call $updateBall
        (local.get $current_ptr)
        (local.get $width)
        (local.get $height)
        (local.get $radius)
        (local.get $dt)
      )
      
      ;; Увеличиваем счетчик
      (local.set $i (i32.add (local.get $i) (i32.const 1)))
      
      ;; Проверяем условие продолжения
      (br_if $loop (i32.lt_u (local.get $i) (local.get $count)))
    )
  )
)
