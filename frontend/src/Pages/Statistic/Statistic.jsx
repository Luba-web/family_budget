import { useState } from 'react';
import './Statistic.scss';
import Calendar from '../../Components/Calendar/Calendar';

export default function Statistic() {
  const [startDate, setStartDate] = useState(
    new Date(new Date().getTime() - 7 * 24 * 60 * 60 * 1000).toJSON().slice(0, 10),
  ); // week ago
  const [endDate, setEndDate] = useState(new Date().toJSON().slice(0, 10)); // today

  const handleStartDateChange = (date) => {
    const formattedDate = date.toJSON().slice(0, 10);
    setStartDate(formattedDate);
  };

  const handleEndDateChange = (date) => {
    const formattedDate = date.toJSON().slice(0, 10);
    setEndDate(formattedDate);
  };
  return (
    <section className="statistic">
      <Calendar
        startDate={startDate}
        endDate={endDate}
        handleStartDateChange={handleStartDateChange}
        handleEndDateChange={handleEndDateChange}
      />
    </section>
  );
}
