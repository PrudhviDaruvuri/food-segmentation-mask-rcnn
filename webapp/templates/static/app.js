var URL = 'http://localhost:8000'
var res
jQuery(document).ready(function () {
    $("#row_results").hide();
    $('#btn-process').on('click', function () {
        var form_data = new FormData();
        files = $('#input_file').prop('files')
        for (i = 0; i < files.length; i++)
            form_data.append('file', $('#input_file').prop('files')[i]);

        $.ajax({
            url: URL + '/api/process',
            type: "post",
            data: form_data,
            enctype: 'multipart/form-data',
            contentType: false,
            processData: false,
            cache: false,
            beforeSend: function () {
                $(".overlay").show()
                $("#row_results").hide();
                $('#div_details').html('');
            },
        }).done(function (jsondata, textStatus, jqXHR) {
            res = jsondata
            img_url = jsondata['output']
            $('#img_result').attr('src', img_url)
            $("#row_results").show();

            result = res['result']
            for (i = 0; i < result.length; i++) {
                food = result[i][0]
                size = result[i][2]
                r = result[i][3][0]
                g = result[i][3][1]
                b = result[i][3][2]
                $('#div_details').append(`<span style="background-color: rgba(${r},${g},${b},0.4);">${size}% of ${food}</span>`)
            }
            console.log(jsondata)
            $(".overlay").hide()
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $(".overlay").hide()
        });

    })

})