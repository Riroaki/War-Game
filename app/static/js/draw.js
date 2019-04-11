function createLineOption(r) {
    var lineOption = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        toolbox: {
            feature: {
                dataView: { show: true, readOnly: true },
                restore: { show: true },
                saveAsImage: { show: true }
            }
        },
        legend: {
            data: ['胜率'],
            textStyle:{//图例文字的样式
                color:'#FFFFFF',
                fontSize:16
            }
        },
        xAxis: [
            {
                type: 'category',
                data: ["战区一", "战区二", "战区三", "战区四", "战区五", "战区六", "战区七", "战区八", "战区九", "战区十"],
                axisPointer: {
                    type: 'shadow'
                },
                show: false
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '胜率',
                min: 0,
                max: 1,
                interval: 0.1,
                axisLabel: {
                    formatter: '{value}'
                },
                show: false
            }
        ],
        series: [
            {
                name: '胜率',
                type: 'line',
                data: r,
                color: 'rgba(200, 0, 0, 0.8)',
                lineStyle: {
                    normal: {
                        width: 10
                    }
                }
            }
        ]
    };

    return lineOption;
}

function createBarOption(s, r) {
    var max = -1;

    for (var i = 0; i < 10; i++) {
        if (s[i] > max)
            max = s[i];
    }
    max = max / 5 + 1;
    max *= 5;

    var barOption = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        toolbox: {
            feature: {
                dataView: { show: true, readOnly: true },
                magicType: { show: true, type: ['line', 'bar'] },
                restore: { show: true },
                saveAsImage: { show: true }
            }
        },
        legend: {
            data: ['策略', '胜率'],
            textStyle:{//图例文字的样式
                color:'#FFFFFF',
                fontSize:16
            }
        },
        xAxis: [
            {
                type: 'category',
                data: ["战区一", "战区二", "战区三", "战区四", "战区五", "战区六", "战区七", "战区八", "战区九", "战区十"],
                axisPointer: {
                    type: 'shadow'
                },
                show: false
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '策略',
                min: 0,
                max: max,
                interval: 5,
                axisLabel: {
                    formatter: '{value}'
                },
                show: false
            },
            {
                type: 'value',
                name: '胜率',
                min: 0,
                max: 1,
                interval: 0.1,
                axisLabel: {
                    formatter: '{value}'
                },
                show: false
            }
        ],
        series: [
            {
                name: '策略',
                type: 'bar',
                data: s,
                color: 'rgba(255, 255, 0, 1.0)',
                barWidth: 40,
                itemStyle: {
                    normal: {
                        color: '#FFECB5',
                        barBorderRadius: 10
                    },
                    emphasis: {
                        barBorderRadius: 30
                    },
                },
            },
            {
                name: '胜率',
                type: 'line',
                yAxisIndex: 1,
                data: r,
                color: 'rgba(200, 0, 0, 0.8)',
                lineStyle: {
                    normal: {
                        width: 10
                    }
                }
            }
        ]
    };

    return barOption;
}

function drawBar(s, r, id) {
    var myChart = echarts.init(document.getElementById(id));

    // Create a bar option.
    var barOption = createBarOption(s, r);

    // 为echarts对象加载数据
    myChart.setOption(barOption);
}

function drawRadar(r, id) {
    var myChart = echarts.init(document.getElementById(id));
    // var h = document.getElementById('board-radar').style.height;
    // alert(h);

    option = {
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            x: 'center',
            data: ['己方胜率', '他方胜率'],
            textStyle:{//图例文字的样式
                color:'#FFFFFF',
                fontSize:16
            }
        },
        toolbox: {
            show: true,
            feature: {
                mark: { show: true },
                dataView: { show: true, readOnly: true },
                restore: { show: true },
                saveAsImage: { show: true }
            }
        },
        calculable: true,
        polar: [
            {
                indicator: [
                    { text: '战区一', max: 1 },
                    { text: '战区二', max: 1 },
                    { text: '战区三', max: 1 },
                    { text: '战区四', max: 1 },
                    { text: '战区五', max: 1 },
                    { text: '战区六', max: 1 },
                    { text: '战区七', max: 1 },
                    { text: '战区八', max: 1 },
                    { text: '战区九', max: 1 },
                    { text: '战区十', max: 1 },
                ],
                radius: 200
            }
        ],
        series: [
            {
                name: '胜率',
                type: 'radar',
                itemStyle: {
                    normal: {
                        areaStyle: {
                            type: 'default'
                        }
                    }
                },
                data: [
                    {
                        value: r[0],
                        name: '己方胜率',
                        // itemStyle: {
                        //     normal: {
                        //         color: 'rgba(255, 0, 0, 0.5)'
                        //     }
                        // }
                    },
                    {
                        value: r[1],
                        name: '他方胜率',
                        // itemStyle: {
                        //     normal: {
                        //         color: '#B5C334'
                        //     }
                        // }
                    }
                ]
            }
        ]
    };
    myChart.setOption(option);
}

function drawRank(result, rank, time, id_rank, id_time) {
    var p1 = document.getElementById(id_rank);
    var p2 = document.getElementById(id_time);
    var sum = 0;
    for(var i=0;i<10;i++)
        sum += result[i];
    sum = sum.toFixed(2);
    time = time.slice(5, -7);
    p1.innerText = '得分：' + sum.toString() + ' | 排名：' + rank.toString();
    p2.innerText =  '提交时间：' + time;
}

function drawRankWithUserId(result, rank, time, user, round, id_rank, id_time, id_user) {
    var p1 = document.getElementById(id_rank);
    var p2 = document.getElementById(id_time);
    var p3 = document.getElementById(id_user);
    var sum = 0;
    for(var i=0;i<10;i++)
        sum += result[i];
    sum = sum.toFixed(2);
    time = time.slice(5, -7);
    p1.innerText = '得分：' + sum.toString() + ' | 排名：' + rank.toString();
    p2.innerText =  '提交时间：' + time;
    p3.innerText = '提交者：' + user + ' 提交于第' + round.toString() + '轮';
}