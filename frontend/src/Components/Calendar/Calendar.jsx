import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

function Calendar({ startDate, endDate, handleStartDateChange, handleEndDateChange }) {

    return (
        <div>
            <div>
                <DatePicker
                    selected={new Date(startDate)}
                    onChange={handleStartDateChange}
                    selectsStart
                    startDate={new Date(startDate)}
                    endDate={new Date(endDate)}
                    dateFormat="dd-MM-yyyy"
                />
            </div>
            <div>
                <DatePicker
                    selected={new Date(endDate)}
                    onChange={handleEndDateChange}
                    selectsEnd
                    startDate={new Date(startDate)}
                    endDate={new Date(endDate)}
                    minDate={new Date(startDate)}
                    dateFormat="dd-MM-yyyy"
                />
            </div>
        </div>
    )
}
export default Calendar;
