(function( $ ) {

    $.fn.number = function(customOptions) {

        var options = {

            'containerClass' : 'number-style',
            'minus' : 'number-minus',
            'plus' : 'number-plus',
            'containerTag' : 'div',
            'btnTag' : 'span'

        };

        options = $.extend(true, options, customOptions);

        var input = this;

        input.wrap('<' + options.containerTag + ' class="' + options.containerClass + '">');

        var wrapper = input.parent();

        wrapper.prepend('<' + options.btnTag + ' class="' + options.minus + '"></' + options.btnTag + '>');

        var minus = wrapper.find('.' + options.minus);

        wrapper.append('<' + options.btnTag + ' class="' + options.plus + '"></' + options.btnTag + '>');

        var plus = wrapper.find('.' + options.plus);

        var min = input.attr('min');

        var max = input.attr('max');

        var group = input.attr('js-group');

        var clique = input.attr('clique');

        var podesomar = '1';

        if(input.attr('step')){

            var step = +input.attr('step');

        } else {

            var step = 1;

        }

        if(+input.val() <= +min){

            minus.addClass('disabled');

        }

        if(+input.val() >= +max){

            plus.addClass('disabled');

        }

        minus.click(function () {

            var input = $(this).parent().find('input');

            var value = input.val();

            if(+value > +min){

                input.val(+value - step);
                remClique(group);

                if(+input.val() === +min){

                    input.prev('.' + options.minus).addClass('disabled');

                }

                if(input.next('.' + options.plus).hasClass('disabled')){

                    input.next('.' + options.plus).removeClass('disabled')

                }

            } else if(!min){

                input.val(+value - step);

            };
            avaliaClique(group);

        });

        plus.click(function () {

            var input = $(this).parent().find('input');

            var value = input.val();
            //console.log(podemexer);

            var au_clique = input.attr("clique");

            if(+value < +max  && parseInt(au_clique,10) < parseInt(max,10)){

                input.val(+value + step);
                addClique(group);

                if(+input.val() === +max){

                    input.next('.' + options.plus).addClass('disabled');

                }

                if(input.prev('.' + options.minus).hasClass('disabled')){

                    input.prev('.' + options.minus).removeClass('disabled')

                }

            } else if(!max){

                input.val(+value + step);

            };
            avaliaClique(group);

        });
        function avaliaClique(group){
            //console.log(group);
            var onputs= $("input[js-group=" + group + "]");
            var aux_clique = onputs.attr("clique");
            if (parseInt(aux_clique,10) < parseInt(max,10)){
                //console.log('opa tá menor ainda!');
                //console.log(max + ' ' + aux_clique);
                onputs.next('.' + options.plus).removeClass('disabled');
            } else {
                //console.log('Foi!');
                onputs.next('.' + options.plus).addClass('disabled');
            }
            //console.log(aux_clique);
            //console.log(podemexer);
        };
        function addClique(group){
            /*$('input').attr('js-group', group).each(function(){
                console.log(group);
            });*/
            //var onputs= $('input[js-group='+ group + ']');
            //var onputs= $(":number[js-group='id_1']")
            var onputs= $("input[js-group=" + group + "]");
            var aux_clique = $("input[js-group=" + group + "]").attr("clique");
            onputs.attr('clique', parseInt(aux_clique,10) + parseInt(1, 10));
            //console.log(aux_clique);
            //console.log(onputs);

        };
        function remClique(group){
            var onputs= $("input[js-group=" + group + "]");
            var aux_clique = $("input[js-group=" + group + "]").attr("clique");
            onputs.attr('clique', parseInt(aux_clique,10) - parseInt(1, 10));
        };
    };

})(jQuery);