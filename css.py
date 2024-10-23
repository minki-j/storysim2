from fasthtml.common import *

main_css = """

@media only screen and (min-width: 64em) {
    .container {
        width: 700px !important;
    }
}
.main-page-loader{
    display:none;
}
.htmx-request.main-page-loader{
    display:inline;
    transform: translate(-50%, -50%);
    animation: pulse 2s ease-in-out infinite !important;
}
.btn-loader {
    position: relative;
    pointer-events: auto;
    opacity: 1;
}
.htmx-request.btn-loader {
    color: transparent;
    pointer-events: none;
}
.htmx-request.btn-loader::after {
    content: "Loading...";
    position: absolute;
    width: auto;
    height: auto;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #000000;
    font-size: 14px;
    animation: pulse 2s ease-in-out infinite !important;
}
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.2; }
    100% { opacity: 1; }
}
.error-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
.error-modal .error-content {
    padding: 20px;
    border-radius: 5px;
    width: 80%;
    height: 80%;
    overflow: auto;
    position: relative;
    background-color: var(--pico-background-color);
    border: var(--pico-primary-border);
}
.error-modal .error-content .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 24px;
    cursor: pointer;
    border: none;
}

"""
