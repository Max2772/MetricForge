open System

type Operation = Add | Sub | Mul | Div | Fact

type Stats = { Name: string; Values: int list }

module Math =
    let rec factorial n = if n <= 1 then 1 else n * factorial (n - 1)
    let safeDiv a b = if b = 0 then None else Some (a / b)
    let apply op a b =
        match op with
        | Add -> a + b
        | Sub -> a - b
        | Mul -> a * b
        | Div -> match safeDiv a b with Some v -> v | None -> 0
        | Fact -> factorial a

module IO =
    let prompt s = printf "%s" s; Console.ReadLine()
    let readInt s =
        let input = prompt s
        match Int32.TryParse(input) with (true,v) -> Some v | _ -> None

module Analysis =
    let average xs =
        match xs with
        | [] -> None
        | _ -> let sum = List.sum xs in Some (float sum / float (List.length xs))
    let stats name xs = { Name = name; Values = xs }
    let describe s =
        let count = List.length s.Values
        let minv = if count = 0 then None else Some (List.min s.Values)
        let maxv = if count = 0 then None else Some (List.max s.Values)
        let avg = average s.Values
        (s.Name, count, minv, maxv, avg)

let showMenu () =
    printfn "\n=== Меню ==="
    printfn "1. Ввести список чисел"
    printfn "2. Сгенерировать случайный массив"
    printfn "3. Выполнить операции над числами"
    printfn "4. Показать статистику"
    printfn "5. Выход"

[<EntryPoint>]
let main argv =
    let rnd = Random()
    let mutable running = true
    let mutable data : int list = []

    while running do
        showMenu()
        printf "Выбор: "
        match Console.ReadLine() with
        | null -> running <- false
        | choice ->
            match choice.Trim() with
            | "1" ->
                printf "Введите числа через пробел: "
                let line = Console.ReadLine()
                let nums =
                    if String.IsNullOrWhiteSpace(line) then []
                    else
                        line.Split([|' '; '\t'|], StringSplitOptions.RemoveEmptyEntries)
                        |> Array.choose (fun s -> match Int32.TryParse(s) with (true,v) -> Some v | _ -> None)
                        |> Array.toList
                data <- nums
                printfn "Сохранено %d чисел." (List.length data)

            | "2" ->
                match IO.readInt "Размер массива: " with
                | Some n when n > 0 ->
                    let arr = Array.init n (fun _ -> rnd.Next(0,100))
                    data <- Array.toList arr
                    printfn "Сгенерировано: %A" arr
                | _ -> printfn "Некорректный ввод."

            | "3" ->
                if List.isEmpty data then printfn "Нет данных. Сначала добавьте числа."
                else
                    printfn "Выберите операцию: + - * / fact"
                    let opStr = IO.prompt "Операция: "
                    let op = match opStr.Trim() with | "+" -> Add | "-" -> Sub | "*" -> Mul | "/" -> Div | "fact" -> Fact | _ -> Add
                    let results =
                        match op with
                        | Fact -> data |> List.map (fun x -> Math.factorial (abs x))
                        | _ ->
                            data
                            |> List.chunkBySize 2
                            |> List.map (fun pair ->
                                match pair with
                                | a::b::_ -> Math.apply op a b
                                | a::_ -> a
                                | _ -> 0)
                    printfn "Результат: %A" results

            | "4" ->
                let s = Analysis.stats "Данные" data
                let (name,count,minv,maxv,avg) = Analysis.describe s
                printfn "Статистика для %s:" name
                printfn "Кол-во: %d" count
                printfn "Мин: %A" minv
                printfn "Макс: %A" maxv
                printfn "Среднее: %A" avg

            | "5" ->
                printfn "Выход..."
                running <- false

            | _ -> printfn "Неверный выбор."

    0