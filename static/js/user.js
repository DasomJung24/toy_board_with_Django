$(document).on('ready page:load', function() {

    // 필수값들이 채워졌을 때 가입하기 버튼 활성화 
    $(document).on('keyup', 'input', function() {
        var inputName = $(document).find('input[name="username"]').val();
        var inputPassword = $(document).find('input[name="password1"]').val();
        var inputPasswordConfirm = $(document).find('input[name="password2"]').val();
        var nickname = $(document).find('input[name="name"]').val();
        if (inputName && inputPassword && inputPasswordConfirm && nickname && 
            inputPassword == inputPasswordConfirm && inputPassword.length >= 8) {
            $('div.btn-validation-no').hide();
            $('div.btn-validation-ok').show();
        } else {
            $('div.btn-validation-ok').hide();
            $('div.btn-validation-no').show();
        }
    })

    // 마우스 클릭시 비밀번호 길이가 8보다 짧을 때 경고 보이기 
    $(document).on('focus', 'input.password-input', function() {
        var inputWord = $(this).val();
        if (inputWord.length < 8) {
            $(this).parents('td').find('div').show();
        }
    })

    // 비밀번호 입력시 길이가 8보다 짧을 때 경고 보이기 
    $(document).on('keyup', 'input.password-input', function() {
        var inputWord = $(this).val();
        if (inputWord.length >= 8) {
            $(this).parents('td').find('div').hide();
        } else {
            $(this).parents('td').find('div').show();
        }
    })

    // 비밀번호 확인 입력시 첫 비밀번호와 일치하는지 확인하기 
    $(document).on('keyup', 'input.password-confirm', function() {
        var passwordConfirm = $(this).val();
        var firstPassword = $(this).parents('table').find('input[name="password1"]').val();
        if (passwordConfirm == firstPassword) {
            $(this).parents('td').find('div').hide();
        } else {
            $(this).parents('td').find('div').show();
        }
    })

});