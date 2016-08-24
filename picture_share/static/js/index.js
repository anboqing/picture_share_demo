$(function () {
    var oExports = {
        initialize: fInitialize,
        // ��Ⱦ��������
        renderMore: fRenderMore,
        // ��������
        requestData: fRequestData,
        // �򵥵�ģ���滻
        tpl: fTpl
    };
    // ��ʼ��ҳ��ű�
    oExports.initialize();

    function fInitialize() {
        var that = this;
        // ����Ԫ��
        that.listEl = $('#image_list__');
        console.log(that.listEl)
        // ��ʼ������
        //that.uid = window.uid;
        that.page = 1;
        that.pageSize = 5;
        that.listHasNext = true;
        // ���¼�
        $('.js-load-more').on('click', function (oEvent) {
            var oEl = $(oEvent.currentTarget);
            var sAttName = 'data-load';
            // �������������У����Ե���¼�
            if (oEl.attr(sAttName) === '1') {
                return;
            }
            // ���ӱ�ǣ�������������е�Ƶ�����
            oEl.attr(sAttName, '1');
            that.renderMore(function () {
                // ȡ��������λ�����Խ�����һ�μ���
                oEl.removeAttr(sAttName);
                // û���������ؼ��ظ��ఴť
                !that.listHasNext && oEl.hide();
            });
        });
    }

    function fRenderMore(fCb) {
        var that = this;
        // û�и������ݣ�������
        if (!that.listHasNext) {
            return;
        }
        that.requestData({
            uid: that.uid,
            page: that.page + 1,
            pageSize: that.pageSize,
            call: function (oResult) {
                // �Ƿ��и�������
                that.listHasNext = !!oResult.has_next && (oResult.images || []).length > 0;
                // ���µ�ǰҳ��
                that.page++;
                // ��Ⱦ����
                var sHtml = '';
                $.each(oResult.images, function (nIndex, oImage) {
                    sHtml_part1 = that.tpl([
                         '<article class="mod">',
            '<header class="mod-hd">',
                '<time class="time">#{create_date}</time>',
                '<a href="/profile/#{user_id}" class="avatar">',
                 '   <img src="#{head_url}">',
                '</a>',
                '<div class="profile-info">',
                    '<a title="#{}" href="/profile/#{user_id}">#{username}</a>',
                '</div>',
            '</header>',
            '<div class="mod-bd">',
                '<div class="img-box">',
                    '<a href = "/image/#{image_id}">',
                    '<img src="#{image_url}">',
               ' </div>',
           ' </div>',
           ' <div class="mod-ft">',
              '  <ul class="discuss-list">',
                   ' <li class="more-discuss">',
                       ' <a>',
                           ' <span>ȫ�� </span><span class="">#{comment_count}</span>',
                            '<span> ������</span></a>',
                    '</li>'].join(''), oImage);
                    sHtml_part2 = ' ';


                    for (var ni = 0; ni < oImage.comment_count; ni++){
                        dict = {'comment_user_name':oImage.comments[ni].username,
                         'comment_user_id':oImage.comments[ni].user_id,
                            'comment_content':oImage.comments[ni].content };
                        sHtml_part2 += that.tpl([
                        '    <li>',
                            '    <a class="_4zhc5 _iqaka" title="#{comment_user_username}" href="/profile/#{comment_user_id}" data-reactid=".0.1.0.0.0.2.1.2:$comment-17856951190001917.1">#{comment_user_username}</a>',
                            '    <span>',
                            '        <span>#{comment_content}</span>',
                           '     </span>',
                         '   </li>',
                             ].join(''), dict);
                    }

                    sHtml_part3 =    that.tpl([
              '  </ul>',
               ' <section class="discuss-edit">',
                  '  <a class="icon-heart"></a>',
                  '  <form>',
                   '     <input placeholder="�������..." type="text">',
                  '  </form>',
                  '  <button class="more-info">����ѡ��</button>',
               ' </section>',
           ' </div>',

       ' </article>  '
                    ].join(''), oImage);
                    sHtml += sHtml_part1 + sHtml_part2 + sHtml_part3;
                });
                console.log(that.listEl)
                sHtml && that.listEl.append(sHtml);
            },
            error: function () {
                alert('���ִ������Ժ�����');
            },
            always: fCb
        });
    }

    function fRequestData(oConf) {
        var that = this;
        var sUrl = '/images/' + oConf.page + '/' + oConf.pageSize + '/';
        $.ajax({url: sUrl, dataType: 'json'}).done(oConf.call).fail(oConf.error).always(oConf.always);
    }

    function fTpl(sTpl, oData) {
        var that = this;
        sTpl = $.trim(sTpl);
        return sTpl.replace(/#{(.*?)}/g, function (sStr, sName) {
            return oData[sName] === undefined || oData[sName] === null ? '' : oData[sName];
        });
    }
});