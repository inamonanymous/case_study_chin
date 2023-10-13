document.addEventListener("DOMContentLoaded", function () {
    const currentMonthDiv = document.getElementById("currentMonth");
    const prevMonthButton = document.getElementById("prevMonth");
    const nextMonthButton = document.getElementById("nextMonth");

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
                    day++;
                }
                calendarRow.appendChild(td);
            }
            table.appendChild(calendarRow);
            if (day > lastDay) {
                break;
            }
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

    generateCalendar(currentYear, currentMonthIndex);

    function updateDynamicCalendar(year, month) {
        fetch(`/get_calendar/${year}/${month}`)
            .then(response => response.json())
            .then(data => {
                // Update the dynamicCalendar div with the fetched calendar data
                dynamicCalendarDiv.innerHTML = `
                    <h2>${data.month_name}</h2>
                    <pre>${data.calendar}</pre>`;
            })
            .catch(error => console.error('Error fetching calendar data:', error));
    }

    // Call the updateDynamicCalendar function with the desired year and month
    updateDynamicCalendar(2023, 1)
});
