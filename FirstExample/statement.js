const plays = {
  hamlet: { name: 'Hamlet', type: 'tragedy' },
  aslike: { name: 'As You Like It', type: 'comedy' },
  othello: { name: 'Othello', type: 'tragedy' }
};

const invoices = [
  {
    customer: 'BigCo',
    performances: [
      {
        playID: 'hamlet',
        audience: 55
      },
      {
        playID: 'aslike',
        audience: 35
      },
      {
        playID: 'othello',
        audience: 40
      }
    ]
  }
];



const statement = (invoice, plays) => {
  let result = `Statement for ${invoice.customer}\n`;

  for (let perf of invoice.performances) {
    // print line for this order
    result += ` ${playFor(perf).name}: ${usd(amountFor(perf))} (${perf.audience} seats)`;
  }
  result += `Amount owed is ${use(totalAmount())}\n`;
  result += `You earned ${totlaVolumeCredits()} credits\n`;
  return result;

  function playFor(aPerformance){
    return plays[aPerformance.playID];
  };
  
  function usd (aNumber){
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 })
      .format(aNumber / 100);
  };
  
  function amountFor (aPerformance){
    let result = 0;
    switch (playFor(aPerformance).type) {
      case 'tragedy':
        result = 40000;
        if (aPerformance.audience > 30) {
          result += 1000 * (aPerformance.audience - 30);
        }
        break;
      case 'comedy':
        result = 30000;
        if (aPerformance.audience > 20) {
          result += 10000 + 500 * (aPerformance.audience - 20);
        }
        result += 300 * aPerformance.audience;
        break;
      default:
        throw new Error(`unknown type: ${playFor(aPerformance).type}`);
    }
  
    return result;
  };
  
  function volumeCreditsFor(perf) {
    let result = 0;
    result += Math.max(perf.audience - 30, 0);
    if ('comedy' === playFor(perf).type) result += Math.floor(perf.audience / 5);
    return result;
  }
  
  function totlaVolumeCredits() {
    let result = 0;
    for (let perf of invoice.performances) {
      result += volumeCreditsFor(perf);
    }
    return result;
  }
  
  function totalAmount() {
    let result = 0;
    for (let perf of invoices.performances) {
      result += amountFor(perf);
    }
    return result;
  }
};
