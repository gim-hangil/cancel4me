import { Box, Button, Input, Select, Text } from 'dracula-ui';
import { useRef } from 'react';
import { LabelCard } from 'components';
import './BookingView.css';

function BookingView({ onSuccess }) {
  const form_items = [
    [
      {
        label: '출발',
        name: 'departure_station',
        data: ['서울', '대전', '동대구', '부산'],
        renderer: render_select_input,
        ref: useRef(),
      },
      {
        label: '도착',
        name: 'arrival_station',
        data: ['서울', '대전', '동대구', '부산'],
        renderer: render_select_input,
        ref: useRef(),
      },
    ],
    [
      {
        label: '탑승 날짜',
        name: 'date',
        data: 'date',
        ref: useRef(),
      },
      {
        label: '출발 가능 시간',
        name: 'departure_base',
        data: 'time',
        ref: useRef(),
      },
      {
        label: '도착 희망 시간',
        name: 'arrival_limit',
        data: 'time',
        ref: useRef()
      },
    ],
    [
      {
        label: '코레일 ID',
        name: 'korail_id',
        data: 'text',
        ref: useRef()
      },
      {
        label: '코레일 PW',
        name: 'korail_pw',
        data: 'password',
        ref: useRef()
      },
    ],
    [
      {
        label: '전화번호',
        name: 'phone_number',
        data: 'tel',
        renderer: render_tel_input,
        ref: useRef(),
      }
    ]
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
        <Button
          color="purple"
          m="xxs"
          onClick={() => submit_form(form_items, onSuccess)}
        >
          <Text>예약</Text>
        </Button>
      </Box>
    </Box>
  );
}

function render_select_input(stations, ref) {
  return (
    <Select ref={ref} required>
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

function render_tel_input(data, ref) {
  return (
    <Input
      type={data}
      ref={ref}
      pattern="010-[0-9]{4}-[0-9]{4}"
      placeholder="010-0000-0000"
      required
    />
  )
}

function render_simple_input(input_type, ref) {
  return (
    <Input type={input_type} ref={ref} required />
  );
}

function submit_form(form_items, onSuccess) {
  let form_data = {};
  for (let form_row of form_items) {
    for (let input of form_row) {
      form_data[input.name] = input.ref.current.value;
    }
  }
  fetch(process.env.REACT_APP_API_HOST + '/tickets', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      mode: 'cors',
    },
    body: JSON.stringify(form_data),
  }).then((res) => {
    if (res.ok) {
      window.sessionStorage.removeItem('tickets');
      onSuccess();
    }
  });
}

export default BookingView;
