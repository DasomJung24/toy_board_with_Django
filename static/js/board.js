$(document).on('ready page:load', function() {

    // 문자열 포맷하기
    if (!String.prototype.format) {
      String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
          return typeof args[number] != 'undefined'
            ? args[number]
            : match
          ;
        });
      };
    }
  
    // 이미지 캡션 제거하기
    var figcaptionArray = $('figcaption');
    for (let i=0; i < figcaptionArray.length; i++) {
      if (figcaptionArray[i].classList.length) {
        figcaptionArray[i].removeAttribute('class');
        figcaptionArray[i].contentEditable = false;
      }
    }
  
    if ($('figure div').length) {
      $('figure div').remove();
    }
  
    $('figure').removeClass('ck-widget');
  
    // 좋아요 눌렀을 때 변경하기
    $(document).on('click', 'img.heart-btn', function () {
      let post_data = $(this).closest("form").serializeObject();
      var ajax_options = {
        beforeSend: function(xhr, settings) {
          var csrftoken = $(document).attr('cookie').split('=')[1];
          xhr.setRequestHeader('X-CSRFToken', csrftoken)
        },
        url: '/board/posts/favorite',
        method: 'POST',
        data: post_data,
        statusCode: {
          200: function(data, status) {
            let imgSrc = $('img.heart');
            let favCount = $('input.fav-count');
            if (imgSrc.attr('src') === '/static/images/heart.svg') {
              favCount.attr('value', Number(favCount.attr('value'))-1);
              imgSrc.attr('src', '/static/images/favourite-heart.png');
            } else {
              favCount.attr('value', Number(favCount.attr('value'))+1);
              imgSrc.attr('src', '/static/images/heart.svg');
            }
          },
          404: function(xhr, status, error) {
            alert('게시물이 존재하지 않습니다.');
          }
        }
      };
    $.ajax(ajax_options);
    })
  
    // 답글 버튼 눌렀을 때
    $(document).on('click', 'input.reply-btn', function () {
      var commentId = $(this).closest('form').serializeObject().parent_id;
      var reply = $('div.comment-'+commentId);
      if (reply.css('display') === 'none') {
        reply.show();
      } else {
        reply.hide();
      }
    })
  
    // 비회원 수정버튼 눌러 비밀번호 창 열리기
    $(document).on('click', 'span.update-comment-not-user', function (e) {
      var parents = $(this).parents('li');
      parents.find('.textarea-comment').show();
      parents.find('.post-line').hide();
      parents.find('.delete-comment-not-user').hide();
      parents.find('.submit-btn-div').show();
      $(this).hide();
    })
  
    // 비회원 수정 취소 버튼 눌러 비밀번호 창 닫기
    $(document).on('click', 'span.cancel-update', function () {
      var parents = $(this).parents('li');
      parents.find('.post-line').show();
      parents.find('.textarea-comment').hide();
      parents.find('.delete-comment-not-user').show();
      parents.find('.update-comment-not-user').show();
      $(this).parent().hide();
    })
  
    // 비회원 삭제 버튼 눌러 비밀번호 창 열리기
    $(document).on('click', 'span.delete-comment-not-user', function () {
      var parents = $(this).parents('li');
      parents.find('.update-comment-not-user').hide();
      parents.find('.delete-submit').show();
      $(this).hide();
    })
  
    // 비회원 삭제 취소 버튼 눌러 비밀번호 창 닫기
    $(document).on('click', 'span.cancel-delete', function () {
      var parents = $(this).parents('li');
      parents.find('.update-comment-not-user').show();
      parents.find('.delete-comment-not-user').show();
      $(this).parent().hide();
    })
  
    // 회원 수정버튼 눌러 수정하기
    $(document).on('click', 'span.update-comment', function () {
      var parents = $(this).parents('li');
      parents.find('.textarea-comment').show();
      parents.find('.post-line').hide();
      parents.find('.submit-update-user').show();
      parents.find('.delete-comment').hide();
      $(this).hide();
    })
  
    // 회원 수정취소 버튼 눌러서 되돌리기
    $(document).on('click', 'span.update-cancel-user', function () {
      var parents = $(this).parents('li');
      parents.find('.post-line').show();
      parents.find('.textarea-comment').hide();
      parents.find('.update-comment').show();
      parents.find('.delete-comment').show();
      $(this).parent().hide();
    })
  
    // 댓글 수정하기
    $(document).on('click', 'span.submit-update', function() {
      var formData = $(this).closest("form").serializeObject();
      var data = $('textarea.textarea-' + formData.pk + ' ~ .ck .ck-content').html();
      formData['content'] = data;
      if (formData.password1) {
        formData['password'] = formData.password1;
      } else if (formData.password2) {
        formData['password'] = formData.password2;
      }
      var ajax_options = {
        beforeSend: function(xhr, settings) {
          var csrftoken = $(document).attr('cookie').split('=')[1];
          xhr.setRequestHeader('X-CSRFToken', csrftoken)
        },
        url: '/board/posts/' + formData.post + '/comments/update/' + formData.pk,
        method: 'POST',
        data: formData,
        statusCode: {
          200: function(data, status) {
            alert('수정되었습니다.');
            location.reload();
          },
          400: function(xhr, status, error) {
            alert('형식에 맞지 않습니다.');
          },
          403: function (data, status) {
            alert('비밀번호를 다시 확인해 주세요.');
          }
        }
      };
    $.ajax(ajax_options);
    })
  
    // 댓글 삭제하기
    $(document).on('click', '.delete-comment', function() {
      var confirmDelete = confirm('정말 삭제하시겠습니까?');
      if (confirmDelete) {
        var formData = $(this).closest("form").serializeObject();
        var url = $(this).data('url');
        var ajax_options = {
          beforeSend: function(xhr, settings) {
            var csrftoken = $(document).attr('cookie').split('=')[1];
            xhr.setRequestHeader('X-CSRFToken', csrftoken)
          },
          url: url,
          method: 'POST',
          data: formData,
          statusCode: {
            200: function(data, status) {
              alert('삭제되었습니다.');
              location.reload();
            },
            403: function (data, status) {
              alert('비밀번호를 다시 확인해 주세요.');
            },
            404: function(xhr, status, error) {
              alert('해당하는 댓글이 없습니다.');
            }
          }
        };
      $.ajax(ajax_options);
        }
    })
  
    // 게시글 생성하기
    $(document).on('click', 'button.submit-btn', function () {
      var data = $(this).closest("form").serializeObject();
      data['content'] = editor.getData();
      data['content_text'] = editor.ui.view.editable.element.innerText;
      var ajax_options = {
        beforeSend: function (xhr, settings) {
          var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
          xhr.setRequestHeader('X-CSRFToken', csrftoken)
        },
        url: '/board/posts/new',
        method: 'POST',
        data: data,
        statusCode: {
          201: function (data, status) {
            window.location.href = '/board/posts/'+ data.id;
          },
          400: function (data, status) {
            alert('형식에 맞지 않습니다. 다시 작성해주세요.');
          },
          403: function (data, status) {
            alert('비밀번호를 입력해주세요.');
          }
        }
      };
      $.ajax(ajax_options);
    })
  
    // select-box 선택 값 유지
    var selectedOrder = new URLSearchParams(location.search).get('order');
    var selectedSearch = new URLSearchParams(location.search).get('select');
  
    if (selectedOrder === '-created_datetime') {
      $('#-created_datetime').attr('selected', 'selected');
    } else if (selectedOrder === 'title') {
      $('#title').attr('selected', 'selected');
    } else if (selectedOrder === 'created_datetime') {
      $('#created_datetime').attr('selected', 'selected');
    } else if (selectedOrder === '-favorite_count') {
      $('#favorite').attr('selected', 'selected');
    } else if (selectedOrder === '-comment_count') {
      $('#comment').attr('selected', 'selected');
    }
  
    if (selectedSearch === 'title') {
      $('#search-title').attr('selected', 'selected');
    } else if (selectedSearch === 'user') {
      $('#search-user').attr('selected', 'selected');
    } else if (selectedSearch === 'name') {
      $('#search-user').attr('selected', 'selected');
    }
  
  });