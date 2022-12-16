import { Box, Button, Input, Select, Text } from 'dracula-ui';
import { useRef } from 'react';
import { LabelCard } from 'components';
import './BookingView.css';

function BookingView() {
  const form_items = [
    [
      {
        label: '출발',
        data: ['서울', '대전', '동대구', '부산'],
        renderer: render_select_input,
        ref: useRef(),
      },
      {
        label: '도착',
        data: ['서울', '대전', '동대구', '부산'],
        renderer: render_select_input,
        ref: useRef(),
      },
    ],
    [
      { label: '탑승 날짜', data: 'date', ref: useRef()  },
      { label: '출발 가능 시간', data: 'time', ref: useRef()  },
      { label: '도착 희망 시간', data: 'time', ref: useRef()  },
    ],
    [
      { label: '코레일 ID', data: 'text', ref: useRef()  },
      { label: '코레일 PW', data: 'password', ref: useRef()  },
    ],
  ];
  return (
    <Box className="BookingView">
      {
        form_items.map((form_row, idx) =>
          <Box className="row" key={`row-${idx}`}>
            {
              form_row.map(({ label, data, renderer, ref }) => {
                if (renderer === undefined) {
                  renderer = render_simple_input;
                }
                return (
                  <LabelCard label={label} key={label}>
                    { renderer(data, ref) }
                  </LabelCard>
                );
              })
            }
          </Box>
        )
      }
      <Box className="submit">
        <Button color="purple" m="xxs" onClick={() => submit_form(form_items)}>
          <Text>예약</Text>
        </Button>
      </Box>
    </Box>
  );
}

function render_select_input(stations, ref) {
  return (
    <Select ref={ref}>
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

function render_simple_input(input_type, ref) {
  return (
    <Input type={input_type} ref={ref} />
  );
}

function submit_form(form_items) {
  let result = '';
  for (let form_row of form_items) {
    for (let input of form_row) {
      result += `${input.label} : ${input.ref.current.value}\n`;
    }
  }
  alert(result);
}

export default BookingView;
