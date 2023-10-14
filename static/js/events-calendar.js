document.addEventListener("DOMContentLoaded", function () {
    const currentMonthDiv = document.getElementById("currentMonth");
    const prevMonthButton = document.getElementById("prevMonth");
    const nextMonthButton = document.getElementById("nextMonth");
    let events = null;

    let currentYear = new Date().getFullYear();
    let currentMonthIndex = new Date().getMonth();

    function generateCalendar(year, month) {
        // Implement logic to calculate the first day of the month and the number of days in the month
        const firstDay = new Date(year, month, 1).getDay();
        const lastDay = new Date(year, month + 1, 0).getDate();

        // Create the table for the calendar
        const table = document.createElement("table");
        table.classList.add("table");

        // Create the header row with weekday names
        const headerRow = document.createElement("tr");
        const monthYearCell = document.createElement("th");
        monthYearCell.colSpan = 7; // Span the whole row
        monthYearCell.textContent = new Date(year, month, 1).toLocaleString('en-US', { month: 'long' }) + " " + year;
        monthYearCell.classList.add("table-dark");
        headerRow.appendChild(monthYearCell);
        table.appendChild(headerRow);

        // Create the header row with weekday names
        const weekdayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const weekdaysRow = document.createElement("tr");
        weekdayNames.forEach(name => {
            const th = document.createElement("th");
            th.textContent = name;
            th.classList.add("table-dark");
            weekdaysRow.appendChild(th);
        });
        table.appendChild(weekdaysRow);

        // Create the calendar rows
        let day = 1;
        for (let i = 0; i < 6; i++) {
            const calendarRow = document.createElement("tr");
            for (let j = 0; j < 7; j++) {
                const td = document.createElement("td");
                if ((i === 0 && j < firstDay) || day > lastDay) {
                    td.textContent = "";
                } else {
                    td.textContent = day;
                    
                    const formattedDate = `${year}-${(month + 1).toString().padStart(2, '0')}-${td.textContent.padStart(2, '0')}`;
                    if (events) {
                        events.holidays.forEach(holiday => {
                            if (holiday.date === formattedDate) {
                                td.textContent = `${day} - Holiday: ${holiday.reason}`;
                                td.classList.add("holiday-date");
                                td.style.backgroundColor = "violet"
                            }
                            });

                        events.reservations.forEach(reservation => {
                            if (reservation.date === formattedDate) {
                                td.textContent = `${day} - Staff: ${reservation.user_name}`;
                                td.classList.add("reservation-date");
                                td.style.backgroundColor = "green";
                            }
                        });
                    }
                    day++;
                }
                calendarRow.appendChild(td);
            }
            table.appendChild(calendarRow);
        }

        currentMonthDiv.innerHTML = ''; // Clear the content
        currentMonthDiv.appendChild(table);
    }

    // Event listener for the next month button
    nextMonthButton.addEventListener("click", () => {
        currentMonthIndex++;
        if (currentMonthIndex > 11) {
            currentMonthIndex = 0;
            currentYear++;
        }
        generateCalendar(currentYear, currentMonthIndex);
    });

    // Event listener for the previous month button
    prevMonthButton.addEventListener("click", () => {
        currentMonthIndex--;
        if (currentMonthIndex < 0) {
            currentMonthIndex = 11;
            currentYear--;
        }
        generateCalendar(currentYear, currentMonthIndex);
    });

    // Fetch the event and holiday data and update the calendar here
    fetch(`/get_calendar/${currentYear}/${currentMonthIndex}`)
        .then(response => response.json())
        .then(data => {
            events = data.events;
            generateCalendar(currentYear, currentMonthIndex);
        })
        .catch(error => console.error('Error fetching calendar data:', error));
});
