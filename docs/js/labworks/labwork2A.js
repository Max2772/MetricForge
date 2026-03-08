import { CONFIG } from "../config.js";

const API_URL = CONFIG.API_URL;

document.addEventListener("DOMContentLoaded", () => {
    const codeInput = document.getElementById("codeInput");
    const resultEl = document.getElementById("result");

    function initTable() {
        const metrics = {
            "Абсолютная сложность (CL)": 0,
            "Относительная сложность (cl)": 0,
            "Макс. уровень вложенности (CLI)": 0,
            "Всего операторов": 0
        };

        let html = '<h3>Метрики Джилба, Маккейба</h3><table class="table table-bordered"><tbody>';
        for (let key in metrics) {
            html += `<tr><td>${key}</td><td>${metrics[key]}</td></tr>`;
        }
        html += '</tbody></table>';
        resultEl.innerHTML = html;
    }

    initTable();

    async function calculateMetrics() {
        const code = codeInput.value || "";

        if (!code) {
            initTable();
        } else {
            try {
                const response = await fetch(`${API_URL}/labwork/2A`, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        code
                    })
                });

                const data = await response.json();

                let html = '<h3>Метрики Джилба, Маккейба</h3><table class="table table-bordered"><tbody>';

                for (let key in data.metrics) {
                    html += `<tr><td>${key}</td><td>${data.metrics[key]}</td></tr>`;
                }
                html += '</tbody></table>';

                html += '<h5>Операторы (управляющие конструкции)</h5><table class="table table-bordered"><tbody>';
                let i = 1;
                for (let [name, count] of data.operators) {
                    html += `<tr><td>${i}</td><td>${name}</td><td>${count}</td></tr>`;
                    i++;
                }
                html += '</tbody></table>';

                resultEl.innerHTML = html;

            } catch (err) {
                console.error(err);
                resultEl.innerHTML = `<p class="text-danger">Ошибка при обращении к серверу</p>`;
            }
        }
    }

    codeInput.addEventListener("input", calculateMetrics);
});