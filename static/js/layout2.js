document.addEventListener("DOMContentLoaded", function() {
    const logoutButton = document.getElementById("logout_button");

    logoutButton.addEventListener("click", function(event) {
        event.preventDefault(); // 링크의 기본 동작을 막음
        sessionStorage.clear();
        window.location.href = logoutButton.getAttribute("href"); // 로그인 페이지로 이동
    });
});
