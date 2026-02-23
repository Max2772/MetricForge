open System

let add a b =
    a + b

let sub a b =
    a - b

let rec factorial n =
    if n <= 1 then 1
    else n * factorial (n - 1)

[<EntryPoint>]
let main argv =
    let x = 5
    let y = 3
    let z = add x y
    let f = factorial z
    if f > 10 then
        printfn "%d" f
    else
        printfn "%d" 0
    0