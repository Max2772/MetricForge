open System

[<EntryPoint>]
let main argv =
    printf "Введите a: "
    let a = Console.ReadLine() |> int

    printf "Введите b: "
    let mutable b = Console.ReadLine() |> int

    let mutable i = 0

    while i <= a do
        match i with
        | 0 ->
            if a > 10 then
                b <- b + 3
            else
                b <- b - 1

        | 2 ->
            if a % 3 = 0 then
                b <- b * 2
            else
                b <- b + 2

        | 4 ->
            if a < 0 then
                b <- 0
            elif a < 5 then
                b <- b + 5
            elif a < 10 then
                b <- b - 3
            else
                b <- b * 2

        | _ ->
            if i % 2 = 0 then
                b <- b + 1
            else
                b <- b - 1

        i <- i + 1

    printfn "Результат: %d" b
    0