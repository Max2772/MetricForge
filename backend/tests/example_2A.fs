// Функция с вложенными условиями (4 уровня)
let analyzeNumber x =
    if x > 0 then
        if x % 2 = 0 then
            if x % 4 = 0 then
                if x % 8 = 0 then
                    "positive, multiple of 8"
                else
                    "positive, multiple of 4 but not 8"
            else
                "positive even, not multiple of 4"
        else
            "positive odd"
    elif x < 0 then
        if x % 2 = 0 then
            "negative even"
        else
            "negative odd"
    else
        "zero"

// Множественный выбор через match
let describeValue y =
    match y with
    | 0 -> "zero"
    | 1 -> "one"
    | 2 -> "two"
    | _ when y < 0 -> "negative"
    | _ -> "positive"

// Цикл for (перебор элементов)
let sumList lst =
    let mutable total = 0
    for elem in lst do
        total <- total + elem
    total

// Цикл while с логическим оператором &&
let findFirstNegative lst =
    let mutable i = 0
    let mutable found = None
    while i < List.length lst && found.IsNone do
        if lst.[i] < 0 then
            found <- Some lst.[i]
        i <- i + 1
    found

// Вложенные циклы for с условиями (3 уровня)
let processMatrix n =
    let matrix = Array2D.create n n 0
    for i in 0 .. n-1 do
        for j in 0 .. n-1 do
            if i = j then
                matrix.[i, j] <- 1
            elif i < j then
                matrix.[i, j] <- 2
            else
                matrix.[i, j] <- 3
    matrix

[<EntryPoint>]
let main argv =
    // Тест analyzeNumber
    let testNumbers = [ 16; 6; 3; -2; -5; 0 ]
    for n in testNumbers do
        printfn "%d: %s" n (analyzeNumber n)

    printfn ""

    // Тест describeValue
    let values = [ 0; 1; 2; -3; 5 ]
    for v in values do
        printfn "%d: %s" v (describeValue v)

    printfn ""

    // Тест sumList
    let list1 = [1; 2; 3; 4; 5]
    printfn "Sum = %d" (sumList list1)

    printfn ""

    // Тест findFirstNegative
    let list2 = [3; 5; -2; 7; -1]
    match findFirstNegative list2 with
    | Some x -> printfn "First negative: %d" x
    | None -> printfn "No negatives"

    printfn ""

    // Тест processMatrix
    let m = processMatrix 3
    for i in 0 .. 2 do
        for j in 0 .. 2 do
            printf "%d " m.[i, j]
        printfn ""

    0