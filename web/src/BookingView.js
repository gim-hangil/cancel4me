import { Box, Button, Input, Select } from 'dracula-ui';
import LabelCard from './LabelCard';
import './BookingView.css';

function BookingView() {
  return (
    <Box className="BookingView">
      <Box className="row">
        <LabelCard label="출발">
          <Select>
            <option value="default" disabled={true}>
              역을 선택해주세요
            </option>
            <option>서울</option>
            <option>동대구</option>
            <option>부산</option>
          </Select>
        </LabelCard>
        <LabelCard label="도착">
          <Select>
            <option value="default" disabled={true}>
              역을 선택해주세요
            </option>
            <option>서울</option>
            <option>동대구</option>
            <option>부산</option>
          </Select>
        </LabelCard>
      </Box>
      <Box className="row">
        <LabelCard label="탑승 날짜">
          <Input type="date" />
        </LabelCard>
        <LabelCard label="출발 가능 시간">
          <Input type="time" />
        </LabelCard>
        <LabelCard label="도착 희망 시간">
          <Input type="time" />
        </LabelCard>
      </Box>
      <Box className="submit">
        <Button color="purple" m="xxs">예약</Button>
      </Box>
    </Box>
  );
}

export default BookingView;
