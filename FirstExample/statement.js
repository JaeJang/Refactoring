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
  return renderPlainText(createStatementData(invoice, plays));  
};

const createStatementData =(invoice, plays) => {
  const result = {};
  result.customer = invoice.customer;
  result.performances = invoice.performances.map(enrichPerformance);
  result.totalAmount = totalAmount(statementData);
  result.totalVolumeCredits = totlaVolumeCredits(statementData);

  return result;

  function enrichPerformance(aPerformance) {
    const result = Object.assign({}, aPerformance);
    result.play = playFor(result);
    result.amount = amountFor(result);
    return result;
  }

  function playFor(aPerformance) {
    return plays[aPerformance.playID];
  }

  function amountFor (aPerformance){
    let result = 0;
    switch (aPerformance.play.type) {
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
        throw new Error(`unknown type: ${aPerformance.play.type}`);
    }
  
    return result;
  };

  function totlaVolumeCredits(data) {
    return data.performances.reduce((total, p) => total + p.volumeCredits, 0);
  }
  
  function totalAmount(data) {
    return data.performances.reduce((total, p) => total + p.amount , 0);
  }
}

const renderPlainText = (data) => {
  let result = `Statement for ${data.customer}\n`;

  for (let perf of data.performances) {
    // print line for this order
    result += ` ${perf.play.name}: ${usd(perf.amount)} (${perf.audience} seats)`;
  }
  result += `Amount owed is ${use(data.totalAmount)}\n`;
  result += `You earned ${data.totlaVolumeCredits} credits\n`;
  return result;

  function usd (aNumber){
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 })
      .format(aNumber / 100);
  };
}
