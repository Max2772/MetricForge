const ENV = ["127.0.0.1", "localhost"].includes(window.location.hostname) ? "local" : "prod";

export const CONFIG = {
  local: {
    API_URL: "http://127.0.0.1:9000"
  },
  prod: {
    API_URL: "https://nonresilient-lauryn-deliberately.ngrok-free.dev"
  }
}[ENV];