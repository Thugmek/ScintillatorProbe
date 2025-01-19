/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usb_device.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "usbd_cdc_if.h"
#include <string.h>
#include <math.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
typedef struct GcodeArgument {
    char name;
    float value;
} GcodeArgument;

typedef struct Gcode {
    int valid;
    char letter;
    int number;
    int arg_len;
    GcodeArgument arguments[32];
} Gcode;
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
#define ADC_TO_VOLTAGE 0.7510653409
#define MAX_PWM 1200

#define PID_P 0.0
#define PID_I 0.0000006
#define PID_D 555.55

#define MAX_INTEGRATOR (1/PID_I)
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;

TIM_HandleTypeDef htim1;

/* USER CODE BEGIN PV */
int pwm_value = 0;
long report_decimator_counter = 0;

float target_voltage = 0.0;

float pid_last_err = 0.0;
float pid_integrator = 0.0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_TIM1_Init(void);
static void MX_ADC1_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
uint8_t TxBuffer[] = "Hello World! From STM32 USB CDC Device To Virtual COM Port\r\n";
uint8_t TxBufferLen = sizeof(TxBuffer);
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USB_DEVICE_Init();
  MX_TIM1_Init();
  MX_ADC1_Init();
  /* USER CODE BEGIN 2 */
  TIM1->CCR1 = 1400;
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
  HAL_ADC_Start_IT(&hadc1);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	//CDC_Transmit_FS(TxBuffer, TxBufferLen);
	//HAL_Delay(1000);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV1;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC|RCC_PERIPHCLK_USB;
  PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV6;
  PeriphClkInit.UsbClockSelection = RCC_USBCLKSOURCE_PLL_DIV1_5;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */

  /** Common config
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ScanConvMode = ADC_SCAN_DISABLE;
  hadc1.Init.ContinuousConvMode = ENABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 1;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure Regular Channel
  */
  sConfig.Channel = ADC_CHANNEL_0;
  sConfig.Rank = ADC_REGULAR_RANK_1;
  sConfig.SamplingTime = ADC_SAMPLETIME_239CYCLES_5;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};
  TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 0;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 1400;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
  if (HAL_TIM_PWM_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
  sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
  sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;
  sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;
  sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;
  sBreakDeadTimeConfig.DeadTime = 0;
  sBreakDeadTimeConfig.BreakState = TIM_BREAK_DISABLE;
  sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;
  sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;
  if (HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */
  HAL_TIM_MspPostInit(&htim1);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

Gcode parse_gcode(char* buff, int len){
    Gcode gcode;
    gcode.valid = 1;
    gcode.arg_len = 0;
    char* index = buff;

    if(buff[0] >= 'A' && buff[0] <= 'Z'){
        gcode.letter = buff[0];
    }else if(buff[0] >= 'a' && buff[0] <= 'z'){
        gcode.letter = buff[0] - ('a'-'A');
    }else{
        gcode.valid = 0;
        return gcode;
    }
    index++;

    gcode.number = 0;
    while(index < buff+len){
        if(*index >= '0' && *index <= '9'){
            gcode.number = gcode.number*10 + (*index - '0');
        }else if (*index == ' ' || *index == '\n'){
            index++;
            break;
        }else{
            gcode.valid = 0;
            return gcode;
        }
        index++;
    }

    int arg_index = -1;
    int inside_arg = 0;
    int decimals = 0;
    while(index < buff+len){
        if(inside_arg){
            if(*index >= '0' && *index <= '9'){
                if(decimals == 0){
                    gcode.arguments[arg_index].value = gcode.arguments[arg_index].value*10 + (*index - '0');
                }else{
                    gcode.arguments[arg_index].value = gcode.arguments[arg_index].value + ((float)(*index - '0') * pow(0.1,decimals));
                    decimals++;
                }
            }else if(*index == '.'){
                if(decimals > 0){
                    gcode.valid = 0;
                    return gcode;
                }
                decimals = 1;
            }else if (*index == ' '){
                decimals = 0;
                inside_arg = 0;
            }else if(*index == '\n'){
                return gcode;
            }else{
                gcode.valid = 0;
                return gcode;
            }
        }else{
            if(*index >= 'A' && *index <= 'Z'){
                arg_index++;
                gcode.arguments[arg_index].name = *index;
                gcode.arguments[arg_index].value = 0;
                gcode.arg_len = arg_index+1;
                inside_arg = 1;
            }else if(*index >= 'a' && *index <= 'z'){
                arg_index++;
                gcode.arguments[arg_index].name = *index - ('a' - 'A');
                gcode.arguments[arg_index].value = 0;
                inside_arg = 1;
            }else if (*index == ' '){

            }else if (*index == '\n'){
                return gcode;
            }else{
                gcode.valid = 0;
                return gcode;
            }

        }
        index++;
    }

    return gcode;
}

int get_gcode_arg(Gcode* gcode, char arg_name, float* out){
	int i = 0;
	while(i<gcode->arg_len){
		if(gcode->arguments[i].name == arg_name){
			*out = gcode->arguments[i].value;
			return 1;
		}
		i++;
	}
	return 0;
}

void USB_CDC_RxHandler(uint8_t* Buf, uint32_t Len)
{
	Gcode gcode = parse_gcode((char*)Buf, Len);

	char TxBuffer[1024];
	if(Buf[0] == 'A'){
		float value = atof((char*)(Buf+1));
		sprintf(TxBuffer, "Received data starting with A and value %f\n", value);
	}else if (Buf[0] == 'B'){
		int value = atoll((char*)(Buf+1));
		sprintf(TxBuffer, "Received data starting with B and value %i\n", value);
	}else{
		sprintf(TxBuffer, "Received data not starting with A or B '%s' with len %i\n", Buf, (int)Len);
	}

	if(gcode.letter == 'P'){
		switch(gcode.number){
			case 1:
				float val = 0;
				if(get_gcode_arg(&gcode,'A', &val)){
					TIM1->CCR1 = 1400-(int)val;
					sprintf(TxBuffer, "Called P1 - set pwm to %ld\n", 1400-TIM1->CCR1);
				}else{
					sprintf(TxBuffer, "Called P1 - actual pwm: %ld\n",1400-TIM1->CCR1);
				}
				break;
			case 2:
				if(get_gcode_arg(&gcode,'V', &target_voltage)){
					sprintf(TxBuffer, "Called P1 - set voltage to %4.2f\n", target_voltage);
				}else{
					sprintf(TxBuffer, "Called P1 - actual voltage: %4.2f\n",target_voltage);
				}
				break;
		}
	}

	uint32_t l = strlen(TxBuffer);
    CDC_Transmit_FS((uint8_t*)TxBuffer, l);
}

//Sample rate 55_555kHz
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
    // Read & Update The ADC Result
	uint32_t raw_adc = HAL_ADC_GetValue(&hadc1);

	float voltage = raw_adc*ADC_TO_VOLTAGE;

	float err = target_voltage-voltage;
	float delta_err = err-pid_last_err;
	pid_last_err = err;
	pid_integrator += err;
	if(pid_integrator > 1666666.0) pid_integrator = 1666666.0;
	if(pid_integrator < -1666666.0) pid_integrator = 1666666.0;

	float pid_output = (err*PID_P) + (pid_integrator*PID_I) + (delta_err*PID_D);
	if(pid_output > 1.0) pid_output = 1.0;
	if(pid_output < 0.0) pid_output = 0.0;

	TIM1->CCR1 = 1400-(int)(pid_output*MAX_PWM);

	if(report_decimator_counter > 15000){
		report_decimator_counter = 0;
		char TxBuffer[1024];
		sprintf(TxBuffer, "Voltage: %04.2fV, PWM: %04ld, PID_O: %01.4f, err: %f, d_err: %f, int: %f\n", voltage, 1400-TIM1->CCR1, pid_output, err, delta_err, pid_integrator);
		uint32_t l = strlen(TxBuffer);
		CDC_Transmit_FS((uint8_t*)TxBuffer, l);
	}
	report_decimator_counter++;
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
