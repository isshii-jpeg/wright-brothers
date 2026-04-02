# Makefile for OECS Firmware
# Target: STM32F103C8T6
# Toolchain: arm-none-eabi-gcc

# Toolchain
PREFIX = arm-none-eabi-
CC = $(PREFIX)gcc
AS = $(PREFIX)gcc -x assembler-with-cpp
CP = $(PREFIX)objcopy
SZ = $(PREFIX)size

# Target
TARGET = oecs_firmware

# Directories
BUILD_DIR = build
CORE_SRC = Core/Src
CORE_INC = Core/Inc
ALGO_DIR = ../algorithm/c

# Sources
C_SOURCES = \
	$(CORE_SRC)/main.c \
	$(ALGO_DIR)/ds_evidence.c

# Includes
C_INCLUDES = \
	-I$(CORE_INC) \
	-I$(ALGO_DIR)

# MCU flags
CPU = -mcpu=cortex-m3
FPU =
FLOAT-ABI =
MCU = $(CPU) -mthumb $(FPU) $(FLOAT-ABI)

# Compiler flags
CFLAGS = $(MCU) -Wall -Wextra -Os -std=c11
CFLAGS += -fdata-sections -ffunction-sections
CFLAGS += $(C_INCLUDES)
CFLAGS += -DSTM32F103xB -DUSE_HAL_DRIVER

# Linker flags
LDFLAGS = $(MCU) -Wl,--gc-sections
LDFLAGS += -T STM32F103C8Tx_FLASH.ld
LDFLAGS += --specs=nano.specs --specs=nosys.specs
LDFLAGS += -lm

# Build rules
all: $(BUILD_DIR)/$(TARGET).elf $(BUILD_DIR)/$(TARGET).hex $(BUILD_DIR)/$(TARGET).bin

OBJECTS = $(addprefix $(BUILD_DIR)/,$(notdir $(C_SOURCES:.c=.o)))
vpath %.c $(sort $(dir $(C_SOURCES)))

$(BUILD_DIR)/%.o: %.c | $(BUILD_DIR)
	$(CC) -c $(CFLAGS) $< -o $@

$(BUILD_DIR)/$(TARGET).elf: $(OBJECTS)
	$(CC) $(OBJECTS) $(LDFLAGS) -o $@
	$(SZ) $@

$(BUILD_DIR)/%.hex: $(BUILD_DIR)/%.elf
	$(CP) -O ihex $< $@

$(BUILD_DIR)/%.bin: $(BUILD_DIR)/%.elf
	$(CP) -O binary -S $< $@

$(BUILD_DIR):
	mkdir -p $@

clean:
	rm -rf $(BUILD_DIR)

flash: $(BUILD_DIR)/$(TARGET).bin
	st-flash write $< 0x8000000

.PHONY: all clean flash
