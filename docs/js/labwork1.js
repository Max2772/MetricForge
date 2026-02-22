document.addEventListener("DOMContentLoaded", () => {
    const codeInput = document.getElementById("codeInput");
    const resultEl = document.getElementById("result");

    function initTable() {
        const metrics = {
            "η1 (уникальные операторы)": 0,
            "η2 (уникальные операнды)": 0,
            "N1 (всего операторов)": 0,
            "N2 (всего операндов)": 0,
            "Словарь программы": 0,
            "Длина программы": 0,
            "Объем программы": 0
        };

        let html = '<h3>Метрики Холстеда</h3><table class="table table-bordered"><tbody>';
        for (let key in metrics) {
            html += `<tr><td>${key}</td><td>${metrics[key]}</td></tr>`;
        }
        html += '</tbody></table>';
        resultEl.innerHTML = html;
    }

    initTable();

    async function calculateMetrics() {
        const code = codeInput.value || "";

        try {
            const response = await fetch("https://nonresilient-lauryn-deliberately.ngrok-free.dev/labwork/1", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ labwork_id: 1, code })
            });

            const data = await response.json();

            if (data.status === "Не готово") {
                resultEl.innerHTML = `<p class="text-warning">Лабораторная 1 ещё не готова</p>`;
                return;
            }

            let html = '<h3>Метрики Холстеда</h3><table class="table table-bordered"><tbody>';
            for (let key in data.metrics) {
                html += `<tr><td>${key}</td><td>${data.metrics[key]}</td></tr>`;
            }
            html += '</tbody></table>';

            html += '<h5>Операторы</h5><table class="table table-bordered"><tbody>';
            for (let key in data.operators) {
                html += `<tr><td>${key}</td><td>${data.operators[key]}</td></tr>`;
            }
            html += '</tbody></table>';

            html += '<h5>Операнды</h5><table class="table table-bordered"><tbody>';
            for (let key in data.operands) {
                html += `<tr><td>${key}</td><td>${data.operands[key]}</td></tr>`;
            }
            html += '</tbody></table>';

            resultEl.innerHTML = html;

        } catch (err) {
            console.error(err);
            resultEl.innerHTML = `<p class="text-danger">Ошибка при обращении к серверу</p>`;
        }
    }

    codeInput.addEventListener("input", calculateMetrics);
});