let color = "#777777";
if(localStorage.getItem('theme') === 'dark'){
  color = "#ffffff";
}
else{
  color = "#777777";
}

export const chartsConfig = {
  options:{
    chart: {
      toolbar: {
        show: false,
      },
    },
    title: {
      show: "",
    },
    dataLabels: {
      enabled: false,
    },
    xaxis: {
      axisTicks: {
        show: false,
      },
      axisBorder: {
        show: false,
      },
      labels: {
        style: {
          colors: "#777777",
          fontSize: "13px",
          fontFamily: "inherit",
          fontWeight: 300,
        },
      },
    },
    yaxis: {
      decimalsInFloat: 2,
      labels: {
        style: {
          colors: "#777777",
          fontSize: "13px",
          fontFamily: "inherit",
          fontWeight: 300,

        },
      },
    },
    grid: {
      show: true,
      borderColor: "#dddddd",
      strokeDashArray: 5,
      xaxis: {
        lines: {
          show: true,
        },
      },
      padding: {
        top: 5,
        right: 20,
      },
    },
    fill: {
      opacity: 0.8,
    },
    tooltip: {
      theme: "dark",
    },
    legend: {
      labels: {
        colors: color,
      },
    }
  }
};

export default chartsConfig;
