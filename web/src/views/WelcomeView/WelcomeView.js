import { Box, Card, Paragraph, Text } from 'dracula-ui';
import './WelcomeView.css';

function WelcomeView() {
  return (
    <Box className="WelcomeView">
      <Card color="purpleCyan" p="sm" m="md">
        <Text color="black">π μ·¨μνλΌλ κ°μ ν λΉμ μκ² κΈ°μ°¨νλ₯Ό κ΅¬ν΄λλ¦½λλ€. π</Text>
      </Card>
      <Paragraph align="left"  px="sm">
        <b>μ·¨μνκ° νμν΄</b>λ μνλ μκ°λμ μ½λ μΌ κΈ°μ°¨νλ₯Ό λμ  μλ§€ν΄μ£Όλ μλΉμ€μλλ€.
        μνλ μκ°λμ κΈ°μ°¨νκ° λ§€μ§λμμ λ μ·¨μνλ₯Ό λκ΅¬λ³΄λ€ λΉ λ₯΄κ² μ°Ύμμ μλ§€ν΄λλ¦½λλ€.
      </Paragraph>
      <Paragraph align="left" px="sm">
        μλ§€ ν­μμ μνλ μΌμ μ μλ ₯νμλ©΄ λκΈ°μ΄μ λ±λ‘λκ³ , μ·¨μνκ° μκΈ°λ©΄ μ°¨λ‘λ‘ λ°°μ λ©λλ€.
      </Paragraph>
    </Box>
  );
}

export default WelcomeView;
