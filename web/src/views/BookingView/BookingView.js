import { Box, Button, Input, Select, Text } from 'dracula-ui';
import { LabelCard } from 'components';
import './BookingView.css';

function BookingView() {
  const form_items = [
    [
      { label: '출발', data: ['서울', '부산'], renderer: render_select_input },
      { label: '도착', data: ['서울', '부산'], renderer: render_select_input },
    ],
    [
      { label: '탑승 날짜', data: 'date' },
      { label: '출발 가능 시간', data: 'time' },
      { label: '도착 희망 시간', data: 'time' },
    ],
    [
      { label: '코레일 ID', data: 'text' },
      { label: '코레일 PW', data: 'password' },
    ],
  ];
  return (
    <Box className="BookingView">
      {
        form_items.map((form_row, idx) =>
          <Box className="row" key={`row-${idx}`}>
            {
              form_row.map(({ label, data, renderer }) => {
                if (renderer === undefined) {
                  renderer = render_simple_input;
                }
                return (
                  <LabelCard label={label} key={label}>
                    { renderer(data) }
                  </LabelCard>
                );
              })
            }
          </Box>
        )
      }
    </Box>
  );
}

function render_select_input(stations) {
  return (
    <Select>
      <option value="default" disabled={true}>
        역을 선택해주세요
      </option>
      {
        stations.map((station) =>
          <option key={station}>{station}</option>
        )
      }
    </Select>
  );
}

function render_simple_input(input_type) {
  return (
    <Input type={input_type} />
  );
}

export default BookingView;
