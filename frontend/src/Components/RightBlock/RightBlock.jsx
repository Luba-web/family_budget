import './RightBlock.scss';
import Moneybox from '../Moneybox/Moneybox';
import Template from '../Template/Template';
import RepeatSpend from '../RepeatSpend/RepeatSpend';

export default function RightBlock() {
  return (
    <section className="right-block">
      <Template title="Повторяющиеся расходы">
        <RepeatSpend />
      </Template>
      <Template title="Конверты на накопления">
        <Moneybox />
      </Template>
    </section>
  );
}